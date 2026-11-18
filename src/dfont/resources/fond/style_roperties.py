from __future__ import annotations

from io import SEEK_CUR
from typing import Any

from dfont.utils.stream import Stream


class FondStyleProperties:
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
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any]) -> FondStyleProperties:
        return self.deepcopy()

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

    def deepcopy(self) -> FondStyleProperties:
        return self.copy()
