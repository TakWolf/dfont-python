import pytest

from dfont import NfntFontType


def test_value_1() -> None:
    font_type = NfntFontType.create()
    assert font_type == NfntFontType.DEFAULT
    assert not font_type.has_image_height_table
    assert not font_type.has_glyph_width_table
    assert not font_type.has_font_color_table
    assert not font_type.synthetic
    assert not font_type.has_colors
    assert not font_type.fixed_width
    assert not font_type.do_not_expand
    assert font_type.font_depth_index == 0
    assert font_type.font_depth == 1


def test_value_2() -> None:
    font_type = NfntFontType.create(
        has_image_height_table=True,
        has_glyph_width_table=True,
        has_font_color_table=True,
        synthetic=True,
        has_colors=True,
        fixed_width=True,
        do_not_expand=True,
        font_depth=8,
    )
    assert font_type == NfntFontType(0b_0111_0011_1000_1111)
    assert font_type.has_image_height_table
    assert font_type.has_glyph_width_table
    assert font_type.has_font_color_table
    assert font_type.synthetic
    assert font_type.has_colors
    assert font_type.fixed_width
    assert font_type.do_not_expand
    assert font_type.font_depth_index == 3
    assert font_type.font_depth == 8


def test_has_image_height_table() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.has_image_height_table

    font_type = font_type.replace(has_image_height_table=True)
    assert font_type.has_image_height_table

    font_type = font_type.replace(has_image_height_table=False)
    assert not font_type.has_image_height_table


def test_has_glyph_width_table() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.has_glyph_width_table

    font_type = font_type.replace(has_glyph_width_table=True)
    assert font_type.has_glyph_width_table

    font_type = font_type.replace(has_glyph_width_table=False)
    assert not font_type.has_glyph_width_table


def test_has_font_color_table() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.has_font_color_table

    font_type = font_type.replace(has_font_color_table=True)
    assert font_type.has_font_color_table

    font_type = font_type.replace(has_font_color_table=False)
    assert not font_type.has_font_color_table


def test_synthetic() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.synthetic

    font_type = font_type.replace(synthetic=True)
    assert font_type.synthetic

    font_type = font_type.replace(synthetic=False)
    assert not font_type.synthetic


def test_has_colors() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.has_colors

    font_type = font_type.replace(has_colors=True)
    assert font_type.has_colors

    font_type = font_type.replace(has_colors=False)
    assert not font_type.has_colors


def test_fixed_width() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.fixed_width

    font_type = font_type.replace(fixed_width=True)
    assert font_type.fixed_width

    font_type = font_type.replace(fixed_width=False)
    assert not font_type.fixed_width


def test_do_not_expand() -> None:
    font_type = NfntFontType.DEFAULT
    assert not font_type.do_not_expand

    font_type = font_type.replace(do_not_expand=True)
    assert font_type.do_not_expand

    font_type = font_type.replace(do_not_expand=False)
    assert not font_type.do_not_expand


def test_font_depth() -> None:
    font_type = NfntFontType.DEFAULT
    assert font_type.font_depth == 1
    assert font_type.font_depth_index == 0

    font_type = font_type.replace(font_depth=2)
    assert font_type.font_depth == 2
    assert font_type.font_depth_index == 1

    font_type = font_type.replace(font_depth=4)
    assert font_type.font_depth == 4
    assert font_type.font_depth_index == 2

    font_type = font_type.replace(font_depth=8)
    assert font_type.font_depth == 8
    assert font_type.font_depth_index == 3

    font_type = font_type.replace(font_depth=1)
    assert font_type.font_depth == 1
    assert font_type.font_depth_index == 0

    with pytest.raises(ValueError):
        font_type.replace(font_depth=16)


def test_eq() -> None:
    font_type_1 = NfntFontType.create(
        has_image_height_table=True,
        has_glyph_width_table=True,
        has_font_color_table=True,
        synthetic=True,
        has_colors=True,
        fixed_width=True,
        do_not_expand=True,
        font_depth=8,
    )
    font_type_2 = NfntFontType.create(
        has_image_height_table=True,
        has_glyph_width_table=True,
        has_font_color_table=True,
        synthetic=True,
        has_colors=True,
        fixed_width=True,
        do_not_expand=True,
        font_depth=8,
    )
    assert font_type_1 == font_type_2
