import pytest

from dfont import FondFontStyle


def test_value_1() -> None:
    font_style = FondFontStyle.create()
    assert font_style == FondFontStyle.DEFAULT
    assert font_style.plain
    assert not font_style.bold
    assert not font_style.italic
    assert not font_style.underline
    assert not font_style.outline
    assert not font_style.shadow
    assert not font_style.condensed
    assert not font_style.extended
    assert font_style.font_depth_index == 0
    assert font_style.font_depth == 1


def test_value_2() -> None:
    font_style = FondFontStyle.create(
        bold=True,
        italic=True,
        underline=True,
        outline=True,
        shadow=True,
        condensed=True,
        extended=True,
        font_depth=8,
    )
    assert font_style == FondFontStyle(0b_0000_0011_0111_1111)
    assert not font_style.plain
    assert font_style.bold
    assert font_style.italic
    assert font_style.underline
    assert font_style.outline
    assert font_style.shadow
    assert font_style.condensed
    assert font_style.extended
    assert font_style.font_depth_index == 3
    assert font_style.font_depth == 8


def test_bold() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.bold

    font_style = font_style.replace(bold=True)
    assert font_style.bold

    font_style = font_style.replace(bold=False)
    assert not font_style.bold


def test_italic() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.italic

    font_style = font_style.replace(italic=True)
    assert font_style.italic

    font_style = font_style.replace(italic=False)
    assert not font_style.italic


def test_underline() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.underline

    font_style = font_style.replace(underline=True)
    assert font_style.underline

    font_style = font_style.replace(underline=False)
    assert not font_style.underline


def test_outline() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.outline

    font_style = font_style.replace(outline=True)
    assert font_style.outline

    font_style = font_style.replace(outline=False)
    assert not font_style.outline


def test_shadow() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.shadow

    font_style = font_style.replace(shadow=True)
    assert font_style.shadow

    font_style = font_style.replace(shadow=False)
    assert not font_style.shadow


def test_condensed() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.condensed

    font_style = font_style.replace(condensed=True)
    assert font_style.condensed

    font_style = font_style.replace(condensed=False)
    assert not font_style.condensed


def test_extended() -> None:
    font_style = FondFontStyle.DEFAULT
    assert not font_style.extended

    font_style = font_style.replace(extended=True)
    assert font_style.extended

    font_style = font_style.replace(extended=False)
    assert not font_style.extended


def test_font_depth() -> None:
    font_style = FondFontStyle.DEFAULT
    assert font_style.font_depth == 1
    assert font_style.font_depth_index == 0

    font_style = font_style.replace(font_depth=2)
    assert font_style.font_depth == 2
    assert font_style.font_depth_index == 1

    font_style = font_style.replace(font_depth=4)
    assert font_style.font_depth == 4
    assert font_style.font_depth_index == 2

    font_style = font_style.replace(font_depth=8)
    assert font_style.font_depth == 8
    assert font_style.font_depth_index == 3

    font_style = font_style.replace(font_depth=1)
    assert font_style.font_depth == 1
    assert font_style.font_depth_index == 0

    with pytest.raises(ValueError):
        font_style.replace(font_depth=16)


def test_plain() -> None:
    font_style = FondFontStyle.DEFAULT
    assert font_style.plain

    font_style = font_style.replace(bold=True)
    assert not font_style.plain

    font_style = font_style.replace(bold=False)
    assert font_style.plain

    font_style = font_style.replace(font_depth=8)
    assert font_style.plain


def test_eq() -> None:
    font_style_1 = FondFontStyle.create(
        bold=True,
        italic=True,
        underline=True,
        outline=True,
        shadow=True,
        condensed=True,
        extended=True,
        font_depth=8,
    )
    font_style_2 = FondFontStyle.create(
        bold=True,
        italic=True,
        underline=True,
        outline=True,
        shadow=True,
        condensed=True,
        extended=True,
        font_depth=8,
    )
    assert font_style_1 == font_style_2
