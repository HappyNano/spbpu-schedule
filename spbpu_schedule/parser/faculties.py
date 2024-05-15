from dataclasses import dataclass
import requests
import typing as tp

from bs4 import BeautifulSoup

from spbpu_schedule.storage import config


@dataclass
class Faculty:
    name: str
    href: str


def get(html_content: str) -> tp.List[Faculty]:
    soup = BeautifulSoup(html_content, 'html.parser')
    faculties = [
        Faculty(tag.text, tag['href']) for tag in soup.find_all('a', class_='faculty-list__link')
    ]

    return faculties
