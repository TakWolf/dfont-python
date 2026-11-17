from pathlib import Path

import pytest

from dfont import DFont


@pytest.mark.parametrize(
    ('font_dir', 'font_file_name'),
    [
        ('cozette', 'cozette.dfont'),
        ('cozette', 'cozette_hidpi.dfont'),
        ('cozette', 'cozettecrossedseven.dfont'),
        ('cozette', 'cozettecrossedseven_hidpi.dfont'),
        ('cozette', 'CozetteVector.dfont'),
        ('cozette', 'CozetteVectorBold.dfont'),
        ('cozette', 'CozetteCrossedSevenVector.dfont'),
        ('cozette', 'CozetteCrossedSevenVectorBold.dfont'),
        ('spleen', 'spleen-5x8.dfont'),
        ('spleen', 'spleen-6x12.dfont'),
        ('spleen', 'spleen-8x16.dfont'),
        ('spleen', 'spleen-12x24.dfont'),
        ('spleen', 'spleen-16x32.dfont'),
        ('spleen', 'spleen-32x64.dfont'),
        ('eldur', 'eldur.dfont'),
        ('eldur', 'eldur2x.dfont'),
        ('harfbuzz', 'DFONT.dfont'),
    ],
)
def test_load_save(
        assets_dir: Path,
        font_dir: str,
        font_file_name: str,
        tmp_path: Path,
) -> None:
    load_path = assets_dir.joinpath(font_dir, font_file_name)
    save_path = tmp_path.joinpath(font_file_name)
    font = DFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()
