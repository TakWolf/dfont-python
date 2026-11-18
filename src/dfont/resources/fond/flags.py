from __future__ import annotations

from enum import IntFlag, unique


@unique
class FondFlags(IntFlag):
    """The 16-bit FamRec.ffFlags field controlling font-family behavior.

    Bits 0 and 2-11 are reserved and should be zero in new resources. Raw values
    and replace() retain unspecified bits when working with existing files.

    https://developer.apple.com/library/archive/documentation/mac/Text/Text-269.html
    """

    DEFAULT = 0
    HAS_GLYPH_WIDTH_TABLE = 0b_0000_0000_0000_0010
    IGNORE_FRACT_ENABLE = 0b_0001_0000_0000_0000
    USE_INTEGER_EXTRA_WIDTH = 0b_0010_0000_0000_0000
    IGNORE_FRACTIONAL_WIDTH_TABLE = 0b_0100_0000_0000_0000
    FIXED_WIDTH = 0b_1000_0000_0000_0000

    @staticmethod
    def create(
            has_glyph_width_table: bool = False,
            ignore_fract_enable: bool = False,
            use_integer_extra_width: bool = False,
            ignore_fractional_width_table: bool = False,
            fixed_width: bool = False,
    ) -> FondFlags:
        """
        :param has_glyph_width_table:
            Whether the resource contains a family glyph-width table.
        :param ignore_fract_enable:
            Whether use_integer_extra_width overrides FractEnable for stylistic variations.
        :param use_integer_extra_width:
            Whether stylistic variations use integer extra width rather than fixed-point extra width.
            When ignore_fract_enable is false, fixed-point extra width also requires FractEnable.
        :param ignore_fractional_width_table:
            Whether the family fractional-width table is disabled.
        :param fixed_width:
            Whether the family describes fixed-width rather than proportional fonts.
        """
        return FondFlags.DEFAULT.replace(
            has_glyph_width_table,
            ignore_fract_enable,
            use_integer_extra_width,
            ignore_fractional_width_table,
            fixed_width,
        )

    @property
    def has_glyph_width_table(self) -> bool:
        return bool(self.value & FondFlags.HAS_GLYPH_WIDTH_TABLE.value)

    @property
    def ignore_fract_enable(self) -> bool:
        return bool(self.value & FondFlags.IGNORE_FRACT_ENABLE.value)

    @property
    def use_integer_extra_width(self) -> bool:
        return bool(self.value & FondFlags.USE_INTEGER_EXTRA_WIDTH.value)

    @property
    def ignore_fractional_width_table(self) -> bool:
        return bool(self.value & FondFlags.IGNORE_FRACTIONAL_WIDTH_TABLE.value)

    @property
    def fixed_width(self) -> bool:
        return bool(self.value & FondFlags.FIXED_WIDTH.value)

    def replace(
            self,
            has_glyph_width_table: bool | None = None,
            ignore_fract_enable: bool | None = None,
            use_integer_extra_width: bool | None = None,
            ignore_fractional_width_table: bool | None = None,
            fixed_width: bool | None = None,
    ) -> FondFlags:
        value = self.value
        if has_glyph_width_table is not None:
            value = value | FondFlags.HAS_GLYPH_WIDTH_TABLE.value if has_glyph_width_table else value & ~FondFlags.HAS_GLYPH_WIDTH_TABLE.value
        if ignore_fract_enable is not None:
            value = value | FondFlags.IGNORE_FRACT_ENABLE.value if ignore_fract_enable else value & ~FondFlags.IGNORE_FRACT_ENABLE.value
        if use_integer_extra_width is not None:
            value = value | FondFlags.USE_INTEGER_EXTRA_WIDTH.value if use_integer_extra_width else value & ~FondFlags.USE_INTEGER_EXTRA_WIDTH.value
        if ignore_fractional_width_table is not None:
            value = value | FondFlags.IGNORE_FRACTIONAL_WIDTH_TABLE.value if ignore_fractional_width_table else value & ~FondFlags.IGNORE_FRACTIONAL_WIDTH_TABLE.value
        if fixed_width is not None:
            value = value | FondFlags.FIXED_WIDTH.value if fixed_width else value & ~FondFlags.FIXED_WIDTH.value
        return FondFlags(value)
