from copy import copy, deepcopy

from dfont import NfntResource, NfntFontType


def test_copy() -> None:
    resource_1 = NfntResource(
        id=140,
        font_type=NfntFontType.create(
            has_glyph_width_table=True,
            has_image_height_table=True,
            fixed_width=True,
        ),
        first_char=65,
        last_char=66,
        width_max=1,
        kern_max=-1,
        negated_descent=-1,
        rectangle_width=3,
        rectangle_height=3,
        offset_width_table_location=13,
        ascent=2,
        descent=1,
        leading=1,
        row_words=1,
        bitmap_data=b'\xe0\x00' * 3,
        bitmap_locations=[0, 1, 2, 3],
        offset_widths=[1, 1, 1, 0xFFFF],
        glyph_widths=[256, 256, 256],
        image_heights=[3, 3, 3],
        table_padding=b'\x00\x00',
        extra_data=b'extra',
        name='Test',
        attributes=4,
    )
    resource_2 = copy(resource_1)

    assert resource_1 == resource_2
    assert resource_1 is not resource_2
    assert resource_1.bitmap_locations is resource_2.bitmap_locations
    assert resource_1.offset_widths is resource_2.offset_widths
    assert resource_1.glyph_widths is resource_2.glyph_widths
    assert resource_1.image_heights is resource_2.image_heights


def test_deepcopy() -> None:
    resource_1 = NfntResource(
        id=140,
        font_type=NfntFontType.create(
            has_glyph_width_table=True,
            has_image_height_table=True,
            fixed_width=True,
        ),
        first_char=65,
        last_char=66,
        width_max=1,
        kern_max=-1,
        negated_descent=-1,
        rectangle_width=3,
        rectangle_height=3,
        offset_width_table_location=13,
        ascent=2,
        descent=1,
        leading=1,
        row_words=1,
        bitmap_data=b'\xe0\x00' * 3,
        bitmap_locations=[0, 1, 2, 3],
        offset_widths=[1, 1, 1, 0xFFFF],
        glyph_widths=[256, 256, 256],
        image_heights=[3, 3, 3],
        table_padding=b'\x00\x00',
        extra_data=b'extra',
        name='Test',
        attributes=4,
    )
    resource_2 = deepcopy(resource_1)

    assert resource_1 == resource_2
    assert resource_1 is not resource_2
    assert resource_1.bitmap_locations is not resource_2.bitmap_locations
    assert resource_1.offset_widths is not resource_2.offset_widths
    assert resource_1.glyph_widths is not resource_2.glyph_widths
    assert resource_1.image_heights is not resource_2.image_heights


def test_eq() -> None:
    resource_1 = NfntResource(
        id=140,
        font_type=NfntFontType.create(
            has_glyph_width_table=True,
            has_image_height_table=True,
            fixed_width=True,
        ),
        first_char=65,
        last_char=66,
        width_max=1,
        kern_max=-1,
        negated_descent=-1,
        rectangle_width=3,
        rectangle_height=3,
        offset_width_table_location=13,
        ascent=2,
        descent=1,
        leading=1,
        row_words=1,
        bitmap_data=b'\xe0\x00' * 3,
        bitmap_locations=[0, 1, 2, 3],
        offset_widths=[1, 1, 1, 0xFFFF],
        glyph_widths=[256, 256, 256],
        image_heights=[3, 3, 3],
        table_padding=b'\x00\x00',
        extra_data=b'extra',
        name='Test',
        attributes=4,
    )
    resource_2 = NfntResource(
        id=140,
        font_type=NfntFontType.create(
            has_glyph_width_table=True,
            has_image_height_table=True,
            fixed_width=True,
        ),
        first_char=65,
        last_char=66,
        width_max=1,
        kern_max=-1,
        negated_descent=-1,
        rectangle_width=3,
        rectangle_height=3,
        offset_width_table_location=13,
        ascent=2,
        descent=1,
        leading=1,
        row_words=1,
        bitmap_data=b'\xe0\x00' * 3,
        bitmap_locations=[0, 1, 2, 3],
        offset_widths=[1, 1, 1, 0xFFFF],
        glyph_widths=[256, 256, 256],
        image_heights=[3, 3, 3],
        table_padding=b'\x00\x00',
        extra_data=b'extra',
        name='Test',
        attributes=4,
    )
    assert resource_1 == resource_2
