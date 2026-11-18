from __future__ import annotations

from typing import Any

from dfont.resources.fond.font_style import FondFontStyle
from dfont.utils.stream import Stream


class FondAssociation:
    """One six-byte AsscEntry mapping a font size and style to a resource ID.

    FOND association tables list outline fonts with size zero before bitmap sizes;
    sizes ascend and plain entries precede styled entries. Serialization preserves
    the caller's record order.

    https://developer.apple.com/library/archive/documentation/mac/Text/Text-271.html

    Attributes:
        font_size:
            Point size of a bitmap font; zero identifies an outline font.
            Corresponds to Apple's fontSize field.
        font_style:
            Combinable style bits; bits 8-9 encode depth for association entries. The depth should match
            bits 2-3 of the referenced NFNT's fontType.
            Corresponds to Apple's fontStyle field.
        font_id:
            Signed 16-bit ID of the referenced 'sfnt', 'NFNT', or 'FONT' resource.
            Corresponds to Apple's fontID field.
    """

    @staticmethod
    def parse(stream: Stream) -> FondAssociation:
        font_size = stream.read_uint16()
        font_style = FondFontStyle(stream.read_uint16())
        font_id = stream.read_int16()
        return FondAssociation(
            font_size,
            font_style,
            font_id,
        )

    font_size: int
    font_style: FondFontStyle
    font_id: int

    def __init__(
            self,
            font_size: int = 0,
            font_style: FondFontStyle = FondFontStyle.DEFAULT,
            font_id: int = 0,
    ) -> None:
        self.font_size = font_size
        self.font_style = font_style
        self.font_id = font_id

    def __copy__(self) -> FondAssociation:
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> FondAssociation:
        return self.deepcopy()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FondAssociation):
            return NotImplemented
        return (self.font_size == other.font_size and
                self.font_style == other.font_style and
                self.font_id == other.font_id)

    def dump(self, stream: Stream) -> int:
        data_start = stream.tell()

        stream.write_uint16(self.font_size)
        stream.write_uint16(self.font_style.value)
        stream.write_int16(self.font_id)

        data_length = stream.tell() - data_start
        return data_length

    def copy(self) -> FondAssociation:
        return FondAssociation(
            self.font_size,
            self.font_style,
            self.font_id,
        )

    def deepcopy(self) -> FondAssociation:
        return self.copy()
