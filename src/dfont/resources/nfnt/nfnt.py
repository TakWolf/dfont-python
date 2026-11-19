from __future__ import annotations

from copy import copy, deepcopy
from typing import Any

from dfont.error import DFontParseError, DFontValidationError
from dfont.resources.nfnt.font_type import NfntFontType
from dfont.resources.resource import Resource
from dfont.utils.stream import Stream

_TAG = 'NFNT'


class NfntResource(Resource):
    """An 'NFNT' bitmap font with a FontRec header and glyph tables.

    The bitmap holds the glyphs side by side. For N character codes in the inclusive
    first_char..last_char range, location and offset/width tables have N + 2 entries:
    characters, the missing glyph, and an end entry. Optional tables have N + 1 entries.
    A zero row_words value represents a stub with no bitmap tables.

    Header: https://developer.apple.com/library/archive/documentation/mac/Text/Text-214.html
    Tables: https://developer.apple.com/library/archive/documentation/mac/Text/Text-250.html

    Attributes:
        font_type:
            The 16-bit font characteristics, optional-table flags, and pixel depth.
            Corresponds to Apple's fontType field.
        first_char:
            First character code in the font's inclusive range.
            Corresponds to Apple's firstChar field.
        last_char:
            Last character code in the font's inclusive range.
            Corresponds to Apple's lastChar field.
        width_max:
            Maximum glyph width, in pixels.
            Corresponds to Apple's widMax field.
        kern_max:
            Horizontal origin-to-left-edge distance; negative for left overhang.
            Corresponds to Apple's kernMax field.
        negated_descent:
            Negated descent, or the high 16 offset bits when positive.
            Corresponds to Apple's nDescent field.
        rectangle_width:
            Width in pixels of the rectangle enclosing superimposed glyphs.
            Corresponds to Apple's fRectWidth field.
        rectangle_height:
            Font rectangle height in pixels, normally ascent plus descent.
            Corresponds to Apple's fRectHeight field.
        offset_width_table_location:
            Low 16 bits of the offset/width-table location, in 16-bit words. The base is this header
            field at payload byte 16. Combine positive nDescent as the high word, then multiply by two
            and add 16 for a payload byte offset.
            Corresponds to Apple's owTLoc field.
        ascent:
            Maximum distance from baseline to the top of the font rectangle, in pixels.
            Corresponds to Apple's ascent field.
        descent:
            Maximum distance below baseline, in pixels.
            Corresponds to Apple's descent field.
        leading:
            Extra vertical spacing between consecutive lines, in pixels.
            Corresponds to Apple's leading field.
        row_words:
            Bitmap scanline length in 16-bit words; zero for a bitmap-less stub.
            Corresponds to Apple's rowWords field.
        bitmap_data:
            Packed bitmap rows, including row-end padding; length is row_words * 2 *
            rectangle_height.
        bitmap_locations:
            Bit offsets into a bitmap row, including the missing glyph and final boundary.
        offset_widths:
            Packed unsigned words: glyph offset in the high byte, integer advance in the low
            byte. Add kern_max to the offset for the left bearing; 0xFFFF marks missing/end entries.
        glyph_widths:
            Optional unsigned 8.8 widths: divide each encoded integer by 256 for pixel units.
            An empty list represents an absent table, as indicated by font_type.
        image_heights:
            Optional packed words: top blank-row count in the high byte, drawn-row count in
            the low byte.
        table_padding:
            Bytes between the location table and offset/width table, retained for layout
            preservation.
        extra_data:
            Uninterpreted bytes after the known tables, including any trailing bytes in a stub.
    """

    @staticmethod
    def parse(
            stream: Stream,
            data_length: int,
            tag: str,
            id: int,
            name: str | None,
            attributes: int = 0,
    ) -> NfntResource:
        if tag != _TAG:
            raise DFontParseError(f'expected resource tag {_TAG!r}, got {tag!r}')

        if data_length < 26:
            raise DFontParseError('truncated NFNT resource')

        data_start = stream.tell()

        font_type = NfntFontType(stream.read_uint16())
        first_char = stream.read_int16()
        last_char = stream.read_int16()
        width_max = stream.read_int16()
        kern_max = stream.read_int16()
        negated_descent = stream.read_int16()
        rectangle_width = stream.read_uint16()
        rectangle_height = stream.read_uint16()
        offset_width_table_location = stream.read_uint16()
        ascent = stream.read_int16()
        descent = stream.read_int16()
        leading = stream.read_int16()
        row_words = stream.read_uint16()

        if row_words > 0:
            if last_char < first_char:
                raise DFontParseError('NFNT last_char precedes first_char')
            # Location and offset/width tables include the missing glyph and an end entry.
            num_table_entries = last_char - first_char + 3

            offset_width_table_offset = offset_width_table_location
            if negated_descent > 0:
                offset_width_table_offset |= negated_descent << 16
            offset_width_table_offset = 16 + offset_width_table_offset * 2

            tables_end_offset = offset_width_table_offset + num_table_entries * 2
            if font_type.has_glyph_width_table:
                tables_end_offset += (num_table_entries - 1) * 2
            if font_type.has_image_height_table:
                tables_end_offset += (num_table_entries - 1) * 2
            if tables_end_offset > data_length:
                raise DFontParseError('NFNT tables exceed resource length')

            bitmap_data_length = row_words * 2 * rectangle_height
            if offset_width_table_offset < 26 + bitmap_data_length + num_table_entries * 2:
                raise DFontParseError('NFNT width table overlaps bitmap or locations')

            bitmap_data = stream.read(bitmap_data_length)
            bitmap_locations = stream.read_uint16_list(num_table_entries)

            table_padding_length = data_start + offset_width_table_offset - stream.tell()
            if table_padding_length < 0:
                raise DFontParseError('NFNT width table overlaps bitmap or locations')
            table_padding = stream.read(table_padding_length)

            offset_widths = stream.read_uint16_list(num_table_entries)

            if font_type.has_glyph_width_table:
                glyph_widths = stream.read_uint16_list(num_table_entries - 1)
            else:
                glyph_widths = []

            if font_type.has_image_height_table:
                image_heights = stream.read_uint16_list(num_table_entries - 1)
            else:
                image_heights = []
        else:
            bitmap_data = b''
            bitmap_locations = None
            offset_widths = None
            glyph_widths = None
            image_heights = None
            table_padding = b''

        extra_data = stream.read(data_length - (stream.tell() - data_start))

        return NfntResource(
            id,
            font_type,
            first_char,
            last_char,
            width_max,
            kern_max,
            negated_descent,
            rectangle_width,
            rectangle_height,
            offset_width_table_location,
            ascent,
            descent,
            leading,
            row_words,
            bitmap_data,
            bitmap_locations,
            offset_widths,
            glyph_widths,
            image_heights,
            table_padding,
            extra_data,
            name,
            attributes,
        )

    font_type: NfntFontType
    first_char: int
    last_char: int
    width_max: int
    kern_max: int
    negated_descent: int
    rectangle_width: int
    rectangle_height: int
    offset_width_table_location: int
    ascent: int
    descent: int
    leading: int
    row_words: int
    bitmap_data: bytes
    bitmap_locations: list[int]
    offset_widths: list[int]
    glyph_widths: list[int]
    image_heights: list[int]
    table_padding: bytes
    extra_data: bytes

    def __init__(
            self,
            id: int,
            font_type: NfntFontType = NfntFontType.DEFAULT,
            first_char: int = 0,
            last_char: int = 255,
            width_max: int = 0,
            kern_max: int = 0,
            negated_descent: int = 0,
            rectangle_width: int = 0,
            rectangle_height: int = 0,
            offset_width_table_location: int = 0,
            ascent: int = 0,
            descent: int = 0,
            leading: int = 0,
            row_words: int = 0,
            bitmap_data: bytes = b'',
            bitmap_locations: list[int] | None = None,
            offset_widths: list[int] | None = None,
            glyph_widths: list[int] | None = None,
            image_heights: list[int] | None = None,
            table_padding: bytes = b'',
            extra_data: bytes = b'',
            name: str | None = None,
            attributes: int = 0,
    ) -> None:
        super().__init__(id, name, attributes)
        self.font_type = font_type
        self.first_char = first_char
        self.last_char = last_char
        self.width_max = width_max
        self.kern_max = kern_max
        self.negated_descent = negated_descent
        self.rectangle_width = rectangle_width
        self.rectangle_height = rectangle_height
        self.offset_width_table_location = offset_width_table_location
        self.ascent = ascent
        self.descent = descent
        self.leading = leading
        self.row_words = row_words
        self.bitmap_data = bitmap_data
        self.bitmap_locations = bitmap_locations if bitmap_locations is not None else []
        self.offset_widths = offset_widths if offset_widths is not None else []
        self.glyph_widths = glyph_widths if glyph_widths is not None else []
        self.image_heights = image_heights if image_heights is not None else []
        self.table_padding = table_padding
        self.extra_data = extra_data

    def __copy__(self) -> NfntResource:
        return NfntResource(
            self.id,
            self.font_type,
            self.first_char,
            self.last_char,
            self.width_max,
            self.kern_max,
            self.negated_descent,
            self.rectangle_width,
            self.rectangle_height,
            self.offset_width_table_location,
            self.ascent,
            self.descent,
            self.leading,
            self.row_words,
            self.bitmap_data,
            self.bitmap_locations,
            self.offset_widths,
            self.glyph_widths,
            self.image_heights,
            self.table_padding,
            self.extra_data,
            self.name,
            self.attributes,
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> NfntResource:
        return NfntResource(
            self.id,
            self.font_type,
            self.first_char,
            self.last_char,
            self.width_max,
            self.kern_max,
            self.negated_descent,
            self.rectangle_width,
            self.rectangle_height,
            self.offset_width_table_location,
            self.ascent,
            self.descent,
            self.leading,
            self.row_words,
            self.bitmap_data,
            self.bitmap_locations.copy(),
            self.offset_widths.copy(),
            self.glyph_widths.copy(),
            self.image_heights.copy(),
            self.table_padding,
            self.extra_data,
            self.name,
            self.attributes,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NfntResource):
            return NotImplemented
        return (super().__eq__(other) and
                self.font_type == other.font_type and
                self.first_char == other.first_char and
                self.last_char == other.last_char and
                self.width_max == other.width_max and
                self.kern_max == other.kern_max and
                self.negated_descent == other.negated_descent and
                self.rectangle_width == other.rectangle_width and
                self.rectangle_height == other.rectangle_height and
                self.offset_width_table_location == other.offset_width_table_location and
                self.ascent == other.ascent and
                self.descent == other.descent and
                self.leading == other.leading and
                self.row_words == other.row_words and
                self.bitmap_data == other.bitmap_data and
                self.bitmap_locations == other.bitmap_locations and
                self.offset_widths == other.offset_widths and
                self.glyph_widths == other.glyph_widths and
                self.image_heights == other.image_heights and
                self.table_padding == other.table_padding and
                self.extra_data == other.extra_data)

    @property
    def tag(self) -> str:
        return _TAG

    def validate(self) -> None:
        if not self.row_words:
            if (
                    self.bitmap_data or
                    self.bitmap_locations or
                    self.offset_widths or
                    self.glyph_widths or
                    self.image_heights or
                    self.table_padding
            ):
                raise DFontValidationError('NFNT stub cannot contain bitmap tables')
            return

        if self.last_char < self.first_char:
            raise DFontValidationError('NFNT last_char precedes first_char')
        num_table_entries = self.last_char - self.first_char + 3

        if len(self.bitmap_data) != self.row_words * 2 * self.rectangle_height:
            raise DFontValidationError('NFNT bitmap size does not match row_words and rectangle_height')

        if len(self.bitmap_locations) != num_table_entries or len(self.offset_widths) != num_table_entries:
            raise DFontValidationError('NFNT location and width counts do not match character range')

        if (any(location < 0 or location > self.row_words * 16 for location in self.bitmap_locations) or
                any(left > right for left, right in zip(self.bitmap_locations, self.bitmap_locations[1:]))):
            raise DFontValidationError('invalid NFNT bitmap locations')

        if len(self.table_padding) % 2:
            raise DFontValidationError('NFNT width table must be word aligned')

        offset_width_table_offset = self.offset_width_table_location
        if self.negated_descent > 0:
            offset_width_table_offset |= self.negated_descent << 16
        offset_width_table_offset = 16 + offset_width_table_offset * 2

        expected_table_offset = 26 + len(self.bitmap_data) + len(self.bitmap_locations) * 2 + len(self.table_padding)
        if offset_width_table_offset != expected_table_offset:
            raise DFontValidationError('NFNT width table offset does not match table layout')

        for present, values in (
                (self.font_type.has_glyph_width_table, self.glyph_widths),
                (self.font_type.has_image_height_table, self.image_heights),
        ):
            if present:
                if len(values) != num_table_entries - 1:
                    raise DFontValidationError('NFNT optional table count does not match character range')
            elif values:
                raise DFontValidationError('NFNT optional table supplied without its font_type flag')

    def dump(self, stream: Stream) -> int:
        self.validate()

        data_start = stream.tell()

        stream.write_uint16(self.font_type.value)
        stream.write_int16(self.first_char)
        stream.write_int16(self.last_char)
        stream.write_int16(self.width_max)
        stream.write_int16(self.kern_max)
        stream.write_int16(self.negated_descent)
        stream.write_uint16(self.rectangle_width)
        stream.write_uint16(self.rectangle_height)
        stream.write_uint16(self.offset_width_table_location)
        stream.write_int16(self.ascent)
        stream.write_int16(self.descent)
        stream.write_int16(self.leading)
        stream.write_uint16(self.row_words)

        if self.row_words:
            stream.write(self.bitmap_data)
            stream.write_uint16_list(self.bitmap_locations)
            stream.write(self.table_padding)
            stream.write_uint16_list(self.offset_widths)
            stream.write_uint16_list(self.glyph_widths)
            stream.write_uint16_list(self.image_heights)

        stream.write(self.extra_data)

        data_length = stream.tell() - data_start
        return data_length

    def copy(self) -> NfntResource:
        return copy(self)

    def deepcopy(self) -> NfntResource:
        return deepcopy(self)
