from copy import copy, deepcopy

from dfont import SfntResource


def test_copy() -> None:
    resource_1 = SfntResource(
        id=128,
        data=b'font',
        name='Test',
        attributes=4,
    )
    resource_2 = copy(resource_1)
    resource_3 = deepcopy(resource_1)

    assert resource_1 == resource_2
    assert resource_1 == resource_3
    assert resource_1 is not resource_2
    assert resource_1 is not resource_3


def test_eq() -> None:
    resource_1 = SfntResource(
        id=128,
        data=b'font',
        name='Test',
        attributes=4,
    )
    resource_2 = SfntResource(
        id=128,
        data=b'font',
        name='Test',
        attributes=4,
    )
    assert resource_1 == resource_2
