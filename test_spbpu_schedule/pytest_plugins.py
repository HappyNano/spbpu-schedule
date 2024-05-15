import pathlib

import pytest

from test_spbpu_schedule import conftest


@pytest.fixture()
def prepare_static():
    def _prepare_static(file: str) -> str:
        for path in conftest.STATIC_PATH:
            if (path / file).exists():
                return str(path / file)
        raise FileNotFoundError(f'File {file} not found in static dirs')

    return _prepare_static


@pytest.fixture()
def read_html():
    def _read_html(html_file_pass: str) -> str:
        with open(html_file_pass, 'r', encoding='utf8') as fin:
            return fin.read()

    return _read_html
