from typing import List
import requests

from bs4 import BeautifulSoup

from config import config


class Group:
    name: str
    key: int

    def __init__(self, name: str, key: int):
        self.name = name
        self.key = key
    
    def __str__(self) -> str:
        return f"Group(name={self.name}, key={self.key})"
    
    def __repr__(self) -> str:
        return self.__str__()


class CourseGroups:
    name: str
    groups: List[Group]
    
    def __init__(self, course_name: str):
        self.name = course_name
        self.groups = []
    
    def add_group(self, group: Group):
        self.groups.append(group)
    
    def __str__(self) -> str:
        return f"CourseGroups(name={self.name}, groups=[" + ", ".join(map(str, self.groups)) + "])"

    def __repr__(self) -> str:
        return self.__str__()


def get(faculty_href: str) -> List[CourseGroups]:
    response = requests.get(config.FACULTIES_URL + faculty_href)

    soup = BeautifulSoup(response.content, 'html.parser')
    courses = soup.find_all(class_='faculty__level')

    arr: List[CourseGroups] = []
    for course in courses:
        arr.append(CourseGroups(course.find('h3').text))
        groups = course.find_all(class_='groups-list__item')
        for group in groups:
            group = group.find('a')
            arr[-1].add_group(Group(group.text, int(group['href'].replace(faculty_href + '/', ''))))

    return arr
