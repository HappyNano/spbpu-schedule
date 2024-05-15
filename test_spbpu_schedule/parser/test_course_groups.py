import pytest

from spbpu_schedule.parser import course_groups


@pytest.mark.parametrize(
    ['faculties_response_file', 'faculty_href', 'expected_res'],
    (
        pytest.param(
            'google.html',
            'asd',
            [],
            id='google'
        ),
        pytest.param(
            'ok_faculties.html',
            'asd',
            '3',
            id='ok',
        ),
    )
)
def test_base(prepare_static, read_html, faculties_response_file, faculty_href, expected_res):
    read_html_path = prepare_static(faculties_response_file)
    html_content = read_html(read_html_path)
    
    assert course_groups.get(faculty_href, html_content) == expected_res
