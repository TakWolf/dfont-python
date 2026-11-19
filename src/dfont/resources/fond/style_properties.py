from __future__ import annotations

from copy import copy, deepcopy
from io import SEEK_CUR
from typing import Any

from dfont.utils.stream import Stream


class FondStyleProperties:
    """Decoded style-dependent extra widths from the nine-word ffProperty array.

    Values describe extra glyph width in pixels at a 1-point size; multiply by the
    requested point size to obtain the corresponding width adjustment. A negative
    value reduces width. Existing intrinsic fonts take precedence over synthesis.
    These values describe width adjustments, not angles or style-selection flags.

    On disk each value is signed 4.12 fixed point (integer divided by 4096).
    The ninth word is unused and is written as zero. plain should also be zero.

    https://developer.apple.com/library/archive/documentation/mac/Text/Text-269.html

    Attributes:
        plain:
            Adjustment for plain text; the specification requires zero.
            Corresponds to Apple's ffProperty[1] entry.
        bold:
            Decoded extra width for bold synthesis.
            Corresponds to Apple's ffProperty[2] entry.
        italic:
            Decoded extra width for italic synthesis.
            Corresponds to Apple's ffProperty[3] entry.
        underline:
            Decoded extra width for underlined text.
            Corresponds to Apple's ffProperty[4] entry.
        outline:
            Decoded extra width for outlined text.
            Corresponds to Apple's ffProperty[5] entry.
        shadow:
            Decoded extra width for shadowed text.
            Corresponds to Apple's ffProperty[6] entry.
        condensed:
            Decoded width adjustment for condensed text.
            Corresponds to Apple's ffProperty[7] entry.
        extended:
            Decoded width adjustment for extended text.
            Corresponds to Apple's ffProperty[8] entry.
    """

    @staticmethod
    def parse(stream: Stream) -> FondStyleProperties:
        plain = stream.read_fixed_4_12()
        bold = stream.read_fixed_4_12()
        italic = stream.read_fixed_4_12()
        underline = stream.read_fixed_4_12()
        outline = stream.read_fixed_4_12()
        shadow = stream.read_fixed_4_12()
        condensed = stream.read_fixed_4_12()
        extended = stream.read_fixed_4_12()
        stream.seek(2, SEEK_CUR)  # reserved
        return FondStyleProperties(
            plain,
            bold,
            italic,
            underline,
            outline,
            shadow,
            condensed,
            extended,
        )

    plain: float
    bold: float
    italic: float
    underline: float
    outline: float
    shadow: float
    condensed: float
    extended: float

    def __init__(
            self,
            plain: float = 0.0,
            bold: float = 0.0,
            italic: float = 0.0,
            underline: float = 0.0,
            outline: float = 0.0,
            shadow: float = 0.0,
            condensed: float = 0.0,
            extended: float = 0.0,
    ) -> None:
        self.plain = plain
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.outline = outline
        self.shadow = shadow
        self.condensed = condensed
        self.extended = extended

    def __copy__(self) -> FondStyleProperties:
        return FondStyleProperties(
            self.plain,
            self.bold,
            self.italic,
            self.underline,
            self.outline,
            self.shadow,
            self.condensed,
            self.extended,
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> FondStyleProperties:
        return copy(self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FondStyleProperties):
            return NotImplemented
        return (self.plain == other.plain and
                self.bold == other.bold and
                self.italic == other.italic and
                self.underline == other.underline and
                self.outline == other.outline and
                self.shadow == other.shadow and
                self.condensed == other.condensed and
                self.extended == other.extended)

    def dump(self, stream: Stream) -> int:
        data_start = stream.tell()

        stream.write_fixed_4_12(self.plain)
        stream.write_fixed_4_12(self.bold)
        stream.write_fixed_4_12(self.italic)
        stream.write_fixed_4_12(self.underline)
        stream.write_fixed_4_12(self.outline)
        stream.write_fixed_4_12(self.shadow)
        stream.write_fixed_4_12(self.condensed)
        stream.write_fixed_4_12(self.extended)
        stream.write_uint16(0)  # reserved

        data_length = stream.tell() - data_start
        return data_length

    def copy(self) -> FondStyleProperties:
        return copy(self)

    def deepcopy(self) -> FondStyleProperties:
        return deepcopy(self)
