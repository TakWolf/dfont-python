from copy import copy, deepcopy

from dfont import FondAssociation, FondFontStyle


def test_copy() -> None:
    association_1 = FondAssociation(
        font_size=12,
        font_style=FondFontStyle.create(bold=True, font_depth=2),
        font_id=-128,
    )
    association_2 = copy(association_1)
    association_3 = deepcopy(association_1)

    assert association_1 == association_2
    assert association_1 == association_3
    assert association_1 is not association_2
    assert association_1 is not association_3


def test_eq() -> None:
    association_1 = FondAssociation(
        font_size=12,
        font_style=FondFontStyle.create(bold=True, font_depth=2),
        font_id=-128,
    )
    association_2 = FondAssociation(
        font_size=12,
        font_style=FondFontStyle.create(bold=True, font_depth=2),
        font_id=-128,
    )
    assert association_1 == association_2
