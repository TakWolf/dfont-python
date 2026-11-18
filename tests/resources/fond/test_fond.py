from copy import copy, deepcopy

from dfont import FondResource, FondFlags, FondAssociation, FondFontStyle, FondStyleProperties


def test_copy() -> None:
    resource_1 = FondResource(
        id=128,
        flags=FondFlags.create(
            has_glyph_width_table=True,
            ignore_fract_enable=True,
            fixed_width=True,
        ),
        family_id=128,
        first_char=32,
        last_char=126,
        ascent=4096,
        descent=1024,
        leading=256,
        width_max=2048,
        style_properties=FondStyleProperties(bold=0.125, italic=0.0625),
        international_info=(7, 9),
        version=2,
        associations=[
            FondAssociation(0, FondFontStyle.DEFAULT, 128),
            FondAssociation(12, FondFontStyle.create(bold=True), 140),
        ],
        additional_data=b'\x00' * 12,
        glyph_width_table_offset=0,
        kerning_table_offset=4,
        style_mapping_table_offset=8,
        name='Test',
        attributes=4,
    )
    resource_2 = copy(resource_1)

    assert resource_1 == resource_2
    assert resource_1 is not resource_2
    assert resource_1.style_properties is resource_2.style_properties
    assert resource_1.associations is resource_2.associations


def test_deepcopy() -> None:
    resource_1 = FondResource(
        id=128,
        flags=FondFlags.create(
            has_glyph_width_table=True,
            ignore_fract_enable=True,
            fixed_width=True,
        ),
        family_id=128,
        first_char=32,
        last_char=126,
        ascent=4096,
        descent=1024,
        leading=256,
        width_max=2048,
        style_properties=FondStyleProperties(bold=0.125, italic=0.0625),
        international_info=(7, 9),
        version=2,
        associations=[
            FondAssociation(0, FondFontStyle.DEFAULT, 128),
            FondAssociation(12, FondFontStyle.create(bold=True), 140),
        ],
        additional_data=b'\x00' * 12,
        glyph_width_table_offset=0,
        kerning_table_offset=4,
        style_mapping_table_offset=8,
        name='Test',
        attributes=4,
    )
    resource_2 = deepcopy(resource_1)

    assert resource_1 == resource_2
    assert resource_1 is not resource_2
    assert resource_1.style_properties is not resource_2.style_properties
    assert resource_1.associations is not resource_2.associations

    for association_1, association_2 in zip(resource_1.associations, resource_2.associations):
        assert association_1 is not association_2


def test_eq() -> None:
    resource_1 = FondResource(
        id=128,
        flags=FondFlags.create(
            has_glyph_width_table=True,
            ignore_fract_enable=True,
            fixed_width=True,
        ),
        family_id=128,
        first_char=32,
        last_char=126,
        ascent=4096,
        descent=1024,
        leading=256,
        width_max=2048,
        style_properties=FondStyleProperties(bold=0.125, italic=0.0625),
        international_info=(7, 9),
        version=2,
        associations=[
            FondAssociation(0, FondFontStyle.DEFAULT, 128),
            FondAssociation(12, FondFontStyle.create(bold=True), 140),
        ],
        additional_data=b'\x00' * 12,
        glyph_width_table_offset=0,
        kerning_table_offset=4,
        style_mapping_table_offset=8,
        name='Test',
        attributes=4,
    )
    resource_2 = FondResource(
        id=128,
        flags=FondFlags.create(
            has_glyph_width_table=True,
            ignore_fract_enable=True,
            fixed_width=True,
        ),
        family_id=128,
        first_char=32,
        last_char=126,
        ascent=4096,
        descent=1024,
        leading=256,
        width_max=2048,
        style_properties=FondStyleProperties(bold=0.125, italic=0.0625),
        international_info=(7, 9),
        version=2,
        associations=[
            FondAssociation(0, FondFontStyle.DEFAULT, 128),
            FondAssociation(12, FondFontStyle.create(bold=True), 140),
        ],
        additional_data=b'\x00' * 12,
        glyph_width_table_offset=0,
        kerning_table_offset=4,
        style_mapping_table_offset=8,
        name='Test',
        attributes=4,
    )
    assert resource_1 == resource_2
