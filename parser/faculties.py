from dataclasses import dataclass
import requests

from bs4 import BeautifulSoup

from config import config


@dataclass
class Faculty:
    name: str
    href: str


def get():
    response = requests.get(config.FACULTIES_URL)

    soup = BeautifulSoup(response.content, 'html.parser')
    faculties = [
        Faculty(tag.text, tag['href']) for tag in soup.find_all('a', class_='faculty-list__link')
    ]

    return faculties
