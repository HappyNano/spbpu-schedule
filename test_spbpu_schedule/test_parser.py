import pytest


@pytest.mark.parametrize(
    ['faculties_response_file', 'expected_res'],
    pytest.param(
        'ok_faculties.html',
        '3',
    ),
)
async def test_base(faculties_response_file, expected_res):
