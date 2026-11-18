from copy import copy, deepcopy
from pathlib import Path

from dfont import DFont


def test_copy(assets_dir: Path) -> None:
    font_1 = DFont.load(assets_dir.joinpath('cozette', 'cozette.dfont'))
    font_2 = copy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.resources is font_2.resources


def test_deepcopy(assets_dir: Path) -> None:
    font_1 = DFont.load(assets_dir.joinpath('cozette', 'cozette.dfont'))
    font_2 = deepcopy(font_1)

    assert font_1 == font_2
    assert font_1 is not font_2
    assert font_1.resources is not font_2.resources

    for resource_1, resource_2 in zip(font_1.resources, font_2.resources):
        assert resource_1 is not resource_2


def test_eq(assets_dir: Path) -> None:
    file_path = assets_dir.joinpath('cozette', 'cozette.dfont')
    font_1 = DFont.load(file_path)
    font_2 = DFont.load(file_path)
    assert font_1 == font_2


def test_eq_application_data() -> None:
    font_1 = DFont(application_data=b'App')
    font_2 = DFont(application_data=b'App'.ljust(128, b'\x00'))
    assert font_1 == font_2
