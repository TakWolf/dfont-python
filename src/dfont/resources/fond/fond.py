from __future__ import annotations

from dfont.error import DFontParseError, DFontDumpError
from dfont.resources.fond.association import FondAssociation
from dfont.resources.fond.flags import FondFlags
from dfont.resources.fond.style_roperties import FondStyleProperties
from dfont.resources.resource import Resource
from dfont.utils.stream import Stream

_TAG = 'FOND'


class FondResource(Resource):
    @staticmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> FondResource:
        if tag != _TAG:
            raise DFontParseError(f'expected resource tag {_TAG!r}, got {tag!r}')

        if data_length < 54:
            raise DFontParseError('truncated FOND resource')

        data_start = stream.tell()

        flags = FondFlags(stream.read_uint16())
        family_id = stream.read_int16()
        first_char = stream.read_int16()
        last_char = stream.read_int16()
        ascent = stream.read_int16()
        descent = stream.read_int16()
        leading = stream.read_int16()
        width_max = stream.read_int16()

        resource_table_offsets = stream.read_uint32_list(3)
        style_properties = FondStyleProperties.parse(stream)
        international_info = tuple(stream.read_int16_list(2))
        version = stream.read_uint16()

        num_associations = stream.read_uint16() + 1
        if 54 + 6 * num_associations > data_length:
            raise DFontParseError('FOND associations exceed resource length')
        associations = [
            FondAssociation.parse(stream)
            for _ in range(num_associations)
        ]

        additional_data = stream.read(data_length - (stream.tell() - data_start))
        additional_data_offset = 54 + 6 * num_associations
        relative_table_offsets = [
            None if offset == 0 else offset - additional_data_offset
            for offset in resource_table_offsets
        ]
        if any(offset is not None and not 0 <= offset < len(additional_data) for offset in relative_table_offsets):
            raise DFontParseError('FOND table offset outside resource')

        # These table offsets are relative to the beginning of additional_data.
        glyph_width_table_offset = relative_table_offsets[0]
        kerning_table_offset = relative_table_offsets[1]
        style_mapping_table_offset = relative_table_offsets[2]

        return FondResource(
            id,
            flags,
            family_id,
            first_char,
            last_char,
            ascent,
            descent,
            leading,
            width_max,
            style_properties,
            international_info,
            version,
            associations,
            additional_data,
            glyph_width_table_offset,
            kerning_table_offset,
            style_mapping_table_offset,
            name,
            attributes,
        )

    flags: FondFlags
    family_id: int
    first_char: int
    last_char: int
    ascent: int
    descent: int
    leading: int
    width_max: int
    style_properties: FondStyleProperties
    international_info: tuple[int, int]
    version: int
    associations: list[FondAssociation]
    additional_data: bytes
    glyph_width_table_offset: int | None
    kerning_table_offset: int | None
    style_mapping_table_offset: int | None

    def __init__(
            self,
            id: int,
            flags: FondFlags = FondFlags.DEFAULT,
            family_id: int = 0,
            first_char: int = 0,
            last_char: int = 255,
            ascent: int = 0,
            descent: int = 0,
            leading: int = 0,
            width_max: int = 0,
            style_properties: FondStyleProperties | None = None,
            international_info: tuple[int, int] = (0, 0),
            version: int = 2,
            associations: list[FondAssociation] | None = None,
            additional_data: bytes = b'',
            glyph_width_table_offset: int | None = None,
            kerning_table_offset: int | None = None,
            style_mapping_table_offset: int | None = None,
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        super().__init__(id, name, attributes)
        self.flags = flags
        self.family_id = family_id
        self.first_char = first_char
        self.last_char = last_char
        self.ascent = ascent
        self.descent = descent
        self.leading = leading
        self.width_max = width_max
        self.style_properties = style_properties if style_properties is not None else FondStyleProperties()
        self.international_info = international_info
        self.version = version
        self.associations = associations if associations is not None else []
        self.additional_data = additional_data
        self.glyph_width_table_offset = glyph_width_table_offset
        self.kerning_table_offset = kerning_table_offset
        self.style_mapping_table_offset = style_mapping_table_offset

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FondResource):
            return NotImplemented
        return (super().__eq__(other) and
                self.flags == other.flags and
                self.family_id == other.family_id and
                self.first_char == other.first_char and
                self.last_char == other.last_char and
                self.ascent == other.ascent and
                self.descent == other.descent and
                self.leading == other.leading and
                self.width_max == other.width_max and
                self.style_properties == other.style_properties and
                self.international_info == other.international_info and
                self.version == other.version and
                self.associations == other.associations and
                self.additional_data == other.additional_data and
                self.glyph_width_table_offset == other.glyph_width_table_offset and
                self.kerning_table_offset == other.kerning_table_offset and
                self.style_mapping_table_offset == other.style_mapping_table_offset)

    @property
    def tag(self) -> str:
        return _TAG

    def dump(self, stream: Stream) -> int:
        num_associations = len(self.associations)
        if not 1 <= num_associations <= 65535:
            raise DFontDumpError('FOND requires between 1 and 65535 associations')

        if len(self.international_info) != 2:
            raise DFontDumpError('FOND requires 2 international values')

        additional_data_offset = 54 + 6 * num_associations
        resource_table_offsets = []
        for offset in (self.glyph_width_table_offset, self.kerning_table_offset, self.style_mapping_table_offset):
            if offset is not None and not 0 <= offset < len(self.additional_data):
                raise DFontDumpError('FOND table offset outside additional_data')
            resource_table_offsets.append(0 if offset is None else additional_data_offset + offset)

        data_start = stream.tell()

        stream.write_uint16(self.flags.value)
        stream.write_int16(self.family_id)
        stream.write_int16(self.first_char)
        stream.write_int16(self.last_char)
        stream.write_int16(self.ascent)
        stream.write_int16(self.descent)
        stream.write_int16(self.leading)
        stream.write_int16(self.width_max)
        stream.write_uint32_list(resource_table_offsets)
        self.style_properties.dump(stream)
        stream.write_int16_list(self.international_info)
        stream.write_uint16(self.version)
        stream.write_uint16(num_associations - 1)
        for association in self.associations:
            association.dump(stream)
        stream.write(self.additional_data)

        data_length = stream.tell() - data_start
        return data_length

    def copy(self) -> FondResource:
        return FondResource(
            self.id,
            self.flags,
            self.family_id,
            self.first_char,
            self.last_char,
            self.ascent,
            self.descent,
            self.leading,
            self.width_max,
            self.style_properties,
            self.international_info,
            self.version,
            self.associations,
            self.additional_data,
            self.glyph_width_table_offset,
            self.kerning_table_offset,
            self.style_mapping_table_offset,
            self.name,
            self.attributes,
        )

    def deepcopy(self) -> FondResource:
        return FondResource(
            self.id,
            self.flags,
            self.family_id,
            self.first_char,
            self.last_char,
            self.ascent,
            self.descent,
            self.leading,
            self.width_max,
            self.style_properties.deepcopy(),
            self.international_info,
            self.version,
            [association.deepcopy() for association in self.associations],
            self.additional_data,
            self.glyph_width_table_offset,
            self.kerning_table_offset,
            self.style_mapping_table_offset,
            self.name,
            self.attributes,
        )
