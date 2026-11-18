from __future__ import annotations

from io import BytesIO, SEEK_CUR
from operator import itemgetter
from os import PathLike
from typing import Any, BinaryIO

from dfont.error import DFontParseError, DFontDumpError
from dfont.resources.factory import RESOURCE_TYPE_REGISTRY
from dfont.resources.raw import RawResource
from dfont.resources.resource import Resource
from dfont.utils.stream import Stream


class DFont:
    """A Macintosh resource file stored in the data fork of a .dfont file.

    Resource payloads are written in resources order; resource-map references are
    grouped by tag. Parsing restores payload order from the recorded data offsets.
    File attributes and each resource's attributes are separate fields.

    Attributes:
        resources:
            Resource payloads and metadata, in their data-area order.
        application_data:
            Application-specific header bytes; at most 128 bytes, padded with zeros on
            output.
        attributes:
            The resource map's 16-bit resource-file attributes, distinct from
            Resource.attributes.
    """

    @staticmethod
    def parse(stream: bytes | bytearray | BinaryIO) -> DFont:
        stream = Stream(stream)

        data_offset = stream.read_uint32()
        map_offset = stream.read_uint32()
        data_length = stream.read_uint32()
        map_length = stream.read_uint32()

        if data_offset < 256 or map_offset < 256 or map_length < 30:
            raise DFontParseError('invalid resource header')
        if data_offset < map_offset + map_length and map_offset < data_offset + data_length:
            raise DFontParseError('resource data and map overlap')

        stream.seek(112, SEEK_CUR)  # system_data
        application_data = stream.read(128)

        stream.seek(map_offset)
        stream.seek(4 * 4, SEEK_CUR)  # data_offset_copy, map_offset_copy, data_length_copy, map_length_copy
        stream.seek(4, SEEK_CUR)  # next_map_handle
        stream.seek(2, SEEK_CUR)  # file_ref_num

        file_attributes = stream.read_uint16()
        type_list_offset = stream.read_uint16()
        name_list_offset = stream.read_uint16()

        if type_list_offset < 28 or type_list_offset + 2 > map_length or name_list_offset > map_length:
            raise DFontParseError('invalid resource list offsets')

        stream.seek(map_offset + type_list_offset)
        num_resource_types_minus_one = stream.read_uint16()
        num_resource_types = 0 if num_resource_types_minus_one == 0xFFFF else num_resource_types_minus_one + 1
        reference_lists_end = type_list_offset + 2 + num_resource_types * 8

        if name_list_offset < reference_lists_end:
            raise DFontParseError('name list overlaps type list')

        resource_entries = []
        resource_tags = set()
        resource_keys = set()
        for type_index in range(num_resource_types):
            stream.seek(map_offset + type_list_offset + 2 + type_index * 8)

            tag = stream.read(4).decode('mac_roman')
            if tag in resource_tags:
                raise DFontParseError(f'duplicate resource type: {tag!r}')
            resource_tags.add(tag)

            num_resources_minus_one = stream.read_uint16()
            if num_resources_minus_one == 0xFFFF:
                raise DFontParseError('resource type has an empty reference list')
            num_resources = num_resources_minus_one + 1

            reference_list_offset = stream.read_uint16()
            reference_list_start = type_list_offset + reference_list_offset
            if reference_list_start < reference_lists_end:
                raise DFontParseError('reference list overlaps type or reference list')

            reference_lists_end = reference_list_start + num_resources * 12
            if reference_lists_end > name_list_offset:
                raise DFontParseError('reference list overlaps name list')

            for resource_index in range(num_resources):
                stream.seek(map_offset + reference_list_start + resource_index * 12)

                resource_id = stream.read_int16()
                if (tag, resource_id) in resource_keys:
                    raise DFontParseError(f'duplicate resource: {(tag, resource_id)!r}')
                resource_keys.add((tag, resource_id))

                name_offset = stream.read_uint16()
                resource_attributes = stream.read_uint8()

                resource_data_offset = stream.read_uint24()
                if resource_data_offset + 4 > data_length:
                    raise DFontParseError('resource length lies outside data area')

                stream.seek(4, SEEK_CUR)  # resource_handle

                name = None
                if name_offset != 0xFFFF:
                    if name_list_offset + name_offset >= map_length:
                        raise DFontParseError('resource name offset lies outside map')

                    stream.seek(map_offset + name_list_offset + name_offset)
                    name_length = stream.read_uint8()

                    if name_list_offset + name_offset + 1 + name_length > map_length:
                        raise DFontParseError('resource name exceeds map')

                    name = stream.read(name_length).decode('mac_roman')

                stream.seek(data_offset + resource_data_offset)

                resource_data_length = stream.read_uint32()
                if resource_data_offset + 4 + resource_data_length > data_length:
                    raise DFontParseError('resource payload exceeds data area')

                resource_class = RESOURCE_TYPE_REGISTRY.get(tag, RawResource)
                resource = resource_class.parse(stream, resource_data_length, tag, resource_id, name, resource_attributes)
                resource_entries.append((resource_data_offset, resource))

        resources = [resource for _, resource in sorted(resource_entries, key=itemgetter(0))]
        return DFont(resources, application_data, file_attributes)

    @staticmethod
    def load(file_path: str | PathLike[str]) -> DFont:
        with open(file_path, 'rb') as file:
            return DFont.parse(file)

    resources: list[Resource]
    application_data: bytes
    attributes: int

    def __init__(
            self,
            resources: list[Resource] | None = None,
            application_data: bytes = b'',
            attributes: int = 0,
    ) -> None:
        self.resources = resources if resources is not None else []
        self.application_data = application_data
        self.attributes = attributes

    def __copy__(self) -> DFont:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> DFont:
        return self.deepcopy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DFont):
            return NotImplemented
        return (self.resources == other.resources and
                self.application_data.ljust(128, b'\x00') == other.application_data.ljust(128, b'\x00') and
                self.attributes == other.attributes)

    def dump(self, stream: BinaryIO) -> None:
        if len(self.application_data) > 128:
            raise DFontDumpError('application_data must not exceed 128 bytes')

        stream = Stream(stream)

        stream.write_nulls(4 * 4)  # Resource header, filled in after writing.
        stream.write_nulls(112)  # system_data
        stream.write(self.application_data)
        stream.write_nulls(128 - len(self.application_data))

        references_by_tag = {}
        encoded_resource_names = []
        data_offset = 256
        name_list_length = 0

        resource_keys = set()

        for resource in self.resources:
            encoded_tag = resource.tag.encode('mac_roman')
            if len(encoded_tag) != 4:
                raise DFontDumpError('resource tag must encode to exactly 4 bytes')

            if (encoded_tag, resource.id) in resource_keys:
                raise DFontDumpError(f'duplicate resource: {(resource.tag, resource.id)!r}')
            resource_keys.add((encoded_tag, resource.id))

            resource_data_offset = stream.tell() - data_offset
            if resource_data_offset > 0xFFFFFF:
                raise DFontDumpError('resource data offset exceeds 24 bits')

            stream.write_uint32(0)  # Resource data length, filled in below.
            resource_data_start = stream.tell()
            resource_data_length = resource.dump(stream)
            stream.seek(resource_data_start - 4)
            stream.write_uint32(resource_data_length)
            stream.seek(resource_data_start + resource_data_length)

            name_offset = 0xFFFF
            if resource.name is not None:
                name_offset = name_list_length
                encoded_name = resource.name.encode('mac_roman')
                if name_offset >= 0xFFFF or len(encoded_name) > 255:
                    raise DFontDumpError('resource name or offset exceeds format limits')
                encoded_resource_names.append(encoded_name)
                name_list_length += 1 + len(encoded_name)
            reference = (resource.id, name_offset, resource.attributes, resource_data_offset)
            references_by_tag.setdefault(encoded_tag, []).append(reference)

        num_resource_types = len(references_by_tag)
        if num_resource_types > 65535:
            raise DFontDumpError('too many resource types')

        map_offset = stream.tell()
        data_length = map_offset - data_offset
        type_list_offset = 28
        name_list_offset = type_list_offset + 2 + num_resource_types * 8 + len(self.resources) * 12

        stream.write_nulls(4 * 4)  # DFont reserves these 16 bytes instead of copying the file header.
        stream.write_uint32(0)  # next_map_handle
        stream.write_int16(0)  # file_ref_num
        stream.write_uint16(self.attributes)
        stream.write_uint16(type_list_offset)
        stream.write_uint16(name_list_offset)
        stream.write_uint16(num_resource_types - 1 if num_resource_types else 0xFFFF)

        reference_list_offset = 2 + num_resource_types * 8
        for encoded_tag, resource_references in references_by_tag.items():
            num_resources = len(resource_references)
            if num_resources > 65535:
                raise DFontDumpError('too many resources of one type')

            stream.write(encoded_tag)
            stream.write_uint16(num_resources - 1)
            stream.write_uint16(reference_list_offset)
            reference_list_offset += num_resources * 12

        for resource_references in references_by_tag.values():
            for resource_id, name_offset, resource_attributes, resource_data_offset in resource_references:
                stream.write_int16(resource_id)
                stream.write_uint16(name_offset)
                stream.write_uint8(resource_attributes)
                stream.write_uint24(resource_data_offset)
                stream.write_uint32(0)  # resource_handle

        for encoded_name in encoded_resource_names:
            stream.write_pascal_bytes(encoded_name)

        map_length = stream.tell() - map_offset
        stream.seek(0)
        stream.write_uint32_list((data_offset, map_offset, data_length, map_length))

    def dump_to_bytes(self) -> bytes:
        stream = BytesIO()
        self.dump(stream)
        return stream.getvalue()

    def save(self, file_path: str | PathLike[str]) -> None:
        with open(file_path, 'wb') as file:
            self.dump(file)

    def copy(self) -> DFont:
        return DFont(
            self.resources,
            self.application_data,
            self.attributes,
        )

    def deepcopy(self) -> DFont:
        return DFont(
            [resource.deepcopy() for resource in self.resources],
            self.application_data,
            self.attributes,
        )
