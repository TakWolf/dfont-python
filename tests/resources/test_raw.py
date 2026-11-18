from copy import copy, deepcopy

from dfont import RawResource


def test_copy() -> None:
    resource_1 = RawResource(
        tag='TEST',
        id=128,
        data=b'payload',
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
    resource_1 = RawResource(
        tag='TEST',
        id=128,
        data=b'payload',
        name='Test',
        attributes=4,
    )
    resource_2 = RawResource(
        tag='TEST',
        id=128,
        data=b'payload',
        name='Test',
        attributes=4,
    )
    assert resource_1 == resource_2
