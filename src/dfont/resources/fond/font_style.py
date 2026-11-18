from __future__ import annotations

from enum import IntFlag, unique
from typing import Final, Literal, get_args

FontDepth = Literal[1, 2, 4, 8]

FONT_DEPTH_OPTIONS: Final[tuple[FontDepth, FontDepth, FontDepth, FontDepth]] = get_args(FontDepth)

_STYLE_MASK = 0b_0000_0000_0111_1111
_FONT_DEPTH_MASK = 0b_0000_0011_0000_0000


@unique
class FondFontStyle(IntFlag):
    """A FOND style code with independent, combinable style bits 0-6.

    In association records, bits 8-9 additionally encode the font's pixel depth.
    Their value must match bits 2-3 in the referenced NFNT's fontType. Other bits
    are retained when reading or replacing existing values.

    Styles: https://developer.apple.com/library/archive/documentation/mac/Text/Text-270.html
    Depth: https://developer.apple.com/library/archive/documentation/mac/Text/Text-271.html
    """

    DEFAULT = 0
    BOLD = 0b_0000_0000_0000_0001
    ITALIC = 0b_0000_0000_0000_0010
    UNDERLINE = 0b_0000_0000_0000_0100
    OUTLINE = 0b_0000_0000_0000_1000
    SHADOW = 0b_0000_0000_0001_0000
    CONDENSED = 0b_0000_0000_0010_0000
    EXTENDED = 0b_0000_0000_0100_0000

    @staticmethod
    def create(
            bold: bool = False,
            italic: bool = False,
            underline: bool = False,
            outline: bool = False,
            shadow: bool = False,
            condensed: bool = False,
            extended: bool = False,
            font_depth: FontDepth = 1,
    ) -> FondFontStyle:
        """
        :param bold:
            Whether the font is bold.
        :param italic:
            Whether the font is italic.
        :param underline:
            Whether the font is underlined.
        :param outline:
            Whether the font is outlined.
        :param shadow:
            Whether the font is shadowed.
        :param condensed:
            Whether the font is condensed.
        :param extended:
            Whether the font is extended.
        :param font_depth:
            The number of bits per pixel, encoded in bits 8 and 9 of an association's fontStyle.
        """
        return FondFontStyle.DEFAULT.replace(
            bold,
            italic,
            underline,
            outline,
            shadow,
            condensed,
            extended,
            font_depth,
        )

    @property
    def plain(self) -> bool:
        return (self.value & _STYLE_MASK) == 0

    @property
    def bold(self) -> bool:
        return bool(self.value & FondFontStyle.BOLD.value)

    @property
    def italic(self) -> bool:
        return bool(self.value & FondFontStyle.ITALIC.value)

    @property
    def underline(self) -> bool:
        return bool(self.value & FondFontStyle.UNDERLINE.value)

    @property
    def outline(self) -> bool:
        return bool(self.value & FondFontStyle.OUTLINE.value)

    @property
    def shadow(self) -> bool:
        return bool(self.value & FondFontStyle.SHADOW.value)

    @property
    def condensed(self) -> bool:
        return bool(self.value & FondFontStyle.CONDENSED.value)

    @property
    def extended(self) -> bool:
        return bool(self.value & FondFontStyle.EXTENDED.value)

    @property
    def font_depth_index(self) -> int:
        return (self.value & _FONT_DEPTH_MASK) >> 8

    @property
    def font_depth(self) -> FontDepth:
        return FONT_DEPTH_OPTIONS[self.font_depth_index]

    def replace(
            self,
            bold: bool | None = None,
            italic: bool | None = None,
            underline: bool | None = None,
            outline: bool | None = None,
            shadow: bool | None = None,
            condensed: bool | None = None,
            extended: bool | None = None,
            font_depth: FontDepth | None = None,
    ) -> FondFontStyle:
        value = self.value
        if bold is not None:
            value = value | FondFontStyle.BOLD.value if bold else value & ~FondFontStyle.BOLD.value
        if italic is not None:
            value = value | FondFontStyle.ITALIC.value if italic else value & ~FondFontStyle.ITALIC.value
        if underline is not None:
            value = value | FondFontStyle.UNDERLINE.value if underline else value & ~FondFontStyle.UNDERLINE.value
        if outline is not None:
            value = value | FondFontStyle.OUTLINE.value if outline else value & ~FondFontStyle.OUTLINE.value
        if shadow is not None:
            value = value | FondFontStyle.SHADOW.value if shadow else value & ~FondFontStyle.SHADOW.value
        if condensed is not None:
            value = value | FondFontStyle.CONDENSED.value if condensed else value & ~FondFontStyle.CONDENSED.value
        if extended is not None:
            value = value | FondFontStyle.EXTENDED.value if extended else value & ~FondFontStyle.EXTENDED.value
        if font_depth is not None:
            value = (value & ~_FONT_DEPTH_MASK) | (FONT_DEPTH_OPTIONS.index(font_depth) << 8)
        return FondFontStyle(value)
