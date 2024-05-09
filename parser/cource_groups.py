from dataclasses import dataclass
import requests
from typing import List

from bs4 import BeautifulSoup

from config import config


@dataclass
class Group:
    name: str
    key: int


@dataclass
class CourseGroups:
    name: str
    groups: List[Group]


def get(faculty_href: str) -> List[CourseGroups]:
    response = requests.get(config.FACULTIES_URL + faculty_href)

    soup = BeautifulSoup(response.content, 'html.parser')
    courses = soup.find_all(class_='faculty__level')

    arr: List[CourseGroups] = []
    for course in courses:
        arr.append(
            CourseGroups(course.find('h3').text, []),
        )
        groups = course.find_all(class_='groups-list__item')
        for group in groups:
            group = group.find('a')
            arr[-1].add_group(
                Group(
                    group.text,
                    int(group['href'].replace(faculty_href + '/', '')),
                )
            )

    return arr
