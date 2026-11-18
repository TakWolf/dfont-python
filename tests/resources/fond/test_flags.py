from dfont import FondFlags


def test_value_1() -> None:
    flags = FondFlags.create()
    assert flags == FondFlags.DEFAULT
    assert not flags.has_glyph_width_table
    assert not flags.ignore_fract_enable
    assert not flags.use_integer_extra_width
    assert not flags.ignore_fractional_width_table
    assert not flags.fixed_width


def test_value_2() -> None:
    flags = FondFlags.create(
        has_glyph_width_table=True,
        ignore_fract_enable=True,
        use_integer_extra_width=True,
        ignore_fractional_width_table=True,
        fixed_width=True,
    )
    assert flags == FondFlags(0b_1111_0000_0000_0010)
    assert flags.has_glyph_width_table
    assert flags.ignore_fract_enable
    assert flags.use_integer_extra_width
    assert flags.ignore_fractional_width_table
    assert flags.fixed_width


def test_has_glyph_width_table() -> None:
    flags = FondFlags.DEFAULT
    assert not flags.has_glyph_width_table

    flags = flags.replace(has_glyph_width_table=True)
    assert flags.has_glyph_width_table

    flags = flags.replace(has_glyph_width_table=False)
    assert not flags.has_glyph_width_table


def test_ignore_fract_enable() -> None:
    flags = FondFlags.DEFAULT
    assert not flags.ignore_fract_enable

    flags = flags.replace(ignore_fract_enable=True)
    assert flags.ignore_fract_enable

    flags = flags.replace(ignore_fract_enable=False)
    assert not flags.ignore_fract_enable


def test_use_integer_extra_width() -> None:
    flags = FondFlags.DEFAULT
    assert not flags.use_integer_extra_width

    flags = flags.replace(use_integer_extra_width=True)
    assert flags.use_integer_extra_width

    flags = flags.replace(use_integer_extra_width=False)
    assert not flags.use_integer_extra_width


def test_ignore_fractional_width_table() -> None:
    flags = FondFlags.DEFAULT
    assert not flags.ignore_fractional_width_table

    flags = flags.replace(ignore_fractional_width_table=True)
    assert flags.ignore_fractional_width_table

    flags = flags.replace(ignore_fractional_width_table=False)
    assert not flags.ignore_fractional_width_table


def test_fixed_width() -> None:
    flags = FondFlags.DEFAULT
    assert not flags.fixed_width

    flags = flags.replace(fixed_width=True)
    assert flags.fixed_width

    flags = flags.replace(fixed_width=False)
    assert not flags.fixed_width


def test_eq() -> None:
    flags_1 = FondFlags.create(
        has_glyph_width_table=True,
        ignore_fract_enable=True,
        use_integer_extra_width=True,
        ignore_fractional_width_table=True,
        fixed_width=True,
    )
    flags_2 = FondFlags.create(
        has_glyph_width_table=True,
        ignore_fract_enable=True,
        use_integer_extra_width=True,
        ignore_fractional_width_table=True,
        fixed_width=True,
    )
    assert flags_1 == flags_2
