from __future__ import annotations

from enum import IntFlag, unique
from typing import Final, Literal, get_args

FontDepth = Literal[1, 2, 4, 8]

FONT_DEPTH_OPTIONS: Final[tuple[FontDepth, FontDepth, FontDepth, FontDepth]] = get_args(FontDepth)

_FONT_DEPTH_MASK = 0b_0000_0000_0000_1100


@unique
class NfntFontType(IntFlag):
    """The 16-bit FontRec.fontType field for an NFNT bitmap font.

    Bits 2-3 encode a depth index: 0, 1, 2, 3 mean 1, 2, 4, 8 bits per pixel.
    New fonts set reserved bit 12 and clear reserved bits 4-6, 10-11, and 15.
    Constructing from a raw integer and replace() preserve unspecified bits.

    https://developer.apple.com/library/archive/documentation/mac/Text/Text-251.html
    """

    DEFAULT = 0b_0001_0000_0000_0000
    HAS_IMAGE_HEIGHT_TABLE = 0b_0000_0000_0000_0001
    HAS_GLYPH_WIDTH_TABLE = 0b_0000_0000_0000_0010
    HAS_FONT_COLOR_TABLE = 0b_0000_0000_1000_0000
    SYNTHETIC = 0b_0000_0001_0000_0000
    HAS_COLORS = 0b_0000_0010_0000_0000
    FIXED_WIDTH = 0b_0010_0000_0000_0000
    DO_NOT_EXPAND = 0b_0100_0000_0000_0000

    @staticmethod
    def create(
            has_image_height_table: bool = False,
            has_glyph_width_table: bool = False,
            has_font_color_table: bool = False,
            synthetic: bool = False,
            has_colors: bool = False,
            fixed_width: bool = False,
            do_not_expand: bool = False,
            font_depth: FontDepth = 1,
    ) -> NfntFontType:
        """
        :param has_image_height_table:
            Whether an image-height table is present.
        :param has_glyph_width_table:
            Whether a fixed-point glyph-width table is present.
        :param has_font_color_table:
            Whether an fctb resource with the same ID is present.
        :param synthetic:
            Whether the font was synthesized for a display configuration.
        :param has_colors:
            Whether the font contains colors other than black.
        :param fixed_width:
            Whether the font is fixed-width rather than proportional.
        :param do_not_expand:
            Whether expansion to the screen depth is disabled.
        :param font_depth:
            The number of bits per pixel, encoded in bits 2 and 3.
        """
        return NfntFontType.DEFAULT.replace(
            has_image_height_table,
            has_glyph_width_table,
            has_font_color_table,
            synthetic,
            has_colors,
            fixed_width,
            do_not_expand,
            font_depth,
        )

    @property
    def has_image_height_table(self) -> bool:
        return bool(self.value & NfntFontType.HAS_IMAGE_HEIGHT_TABLE.value)

    @property
    def has_glyph_width_table(self) -> bool:
        return bool(self.value & NfntFontType.HAS_GLYPH_WIDTH_TABLE.value)

    @property
    def has_font_color_table(self) -> bool:
        return bool(self.value & NfntFontType.HAS_FONT_COLOR_TABLE.value)

    @property
    def synthetic(self) -> bool:
        return bool(self.value & NfntFontType.SYNTHETIC.value)

    @property
    def has_colors(self) -> bool:
        return bool(self.value & NfntFontType.HAS_COLORS.value)

    @property
    def fixed_width(self) -> bool:
        return bool(self.value & NfntFontType.FIXED_WIDTH.value)

    @property
    def do_not_expand(self) -> bool:
        return bool(self.value & NfntFontType.DO_NOT_EXPAND.value)

    @property
    def font_depth_index(self) -> int:
        return (self.value & _FONT_DEPTH_MASK) >> 2

    @property
    def font_depth(self) -> FontDepth:
        return FONT_DEPTH_OPTIONS[self.font_depth_index]

    def replace(
            self,
            has_image_height_table: bool | None = None,
            has_glyph_width_table: bool | None = None,
            has_font_color_table: bool | None = None,
            synthetic: bool | None = None,
            has_colors: bool | None = None,
            fixed_width: bool | None = None,
            do_not_expand: bool | None = None,
            font_depth: FontDepth | None = None,
    ) -> NfntFontType:
        value = self.value
        if has_image_height_table is not None:
            value = value | NfntFontType.HAS_IMAGE_HEIGHT_TABLE.value if has_image_height_table else value & ~NfntFontType.HAS_IMAGE_HEIGHT_TABLE.value
        if has_glyph_width_table is not None:
            value = value | NfntFontType.HAS_GLYPH_WIDTH_TABLE.value if has_glyph_width_table else value & ~NfntFontType.HAS_GLYPH_WIDTH_TABLE.value
        if has_font_color_table is not None:
            value = value | NfntFontType.HAS_FONT_COLOR_TABLE.value if has_font_color_table else value & ~NfntFontType.HAS_FONT_COLOR_TABLE.value
        if synthetic is not None:
            value = value | NfntFontType.SYNTHETIC.value if synthetic else value & ~NfntFontType.SYNTHETIC.value
        if has_colors is not None:
            value = value | NfntFontType.HAS_COLORS.value if has_colors else value & ~NfntFontType.HAS_COLORS.value
        if fixed_width is not None:
            value = value | NfntFontType.FIXED_WIDTH.value if fixed_width else value & ~NfntFontType.FIXED_WIDTH.value
        if do_not_expand is not None:
            value = value | NfntFontType.DO_NOT_EXPAND.value if do_not_expand else value & ~NfntFontType.DO_NOT_EXPAND.value
        if font_depth is not None:
            value = (value & ~_FONT_DEPTH_MASK) | (FONT_DEPTH_OPTIONS.index(font_depth) << 2)
        return NfntFontType(value)
