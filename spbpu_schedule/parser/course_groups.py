from dataclasses import dataclass
import requests
import typing as tp

from bs4 import BeautifulSoup

from spbpu_schedule.storage import config


@dataclass
class Group:
    name: str
    key: int


@dataclass
class CourseGroups:
    name: str
    groups: tp.List[Group]


def get(faculty_href: str, html_content: str) -> tp.List[CourseGroups]:
    soup = BeautifulSoup(html_content, 'html.parser')
    courses = soup.find_all(class_='faculty__level')

    arr: tp.List[CourseGroups] = []
    for course in courses:
        arr.append(
            CourseGroups(course.find('h3').text, []),
        )
        groups = course.find_all(class_='groups-list__item')
        for group in groups:
            group = group.find('a')
            arr[-1].groups.append(
                Group(
                    group.text,
                    int(group['href'].replace(faculty_href + '/', '')),
                )
            )

    return arr
