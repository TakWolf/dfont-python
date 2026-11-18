from copy import copy, deepcopy

from dfont import FondStyleProperties


def test_copy() -> None:
    properties_1 = FondStyleProperties(
        plain=0.0,
        bold=0.125,
        italic=0.25,
        underline=0.5,
        outline=0.75,
        shadow=1.0,
        condensed=-0.125,
        extended=0.125,
    )
    properties_2 = copy(properties_1)
    properties_3 = deepcopy(properties_1)

    assert properties_1 == properties_2
    assert properties_1 == properties_3
    assert properties_1 is not properties_2
    assert properties_1 is not properties_3


def test_eq() -> None:
    properties_1 = FondStyleProperties(
        plain=0.0,
        bold=0.125,
        italic=0.25,
        underline=0.5,
        outline=0.75,
        shadow=1.0,
        condensed=-0.125,
        extended=0.125,
    )
    properties_2 = FondStyleProperties(
        plain=0.0,
        bold=0.125,
        italic=0.25,
        underline=0.5,
        outline=0.75,
        shadow=1.0,
        condensed=-0.125,
        extended=0.125,
    )
    assert properties_1 == properties_2
