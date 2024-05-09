import requests

from bs4 import BeautifulSoup

from config import config


class Faculty:
    def __init__(self, name: str, href: str):
        self.name = name
        self.href = href
    
    @classmethod
    def create(cls, element):
        return Faculty(element.text, element['href'])


def get():
    response = requests.get(config.FACULTIES_URL)

    soup = BeautifulSoup(response.content, 'html.parser')
    faculties = [
        Faculty.create(tag) for tag in soup.find_all('a', class_='faculty-list__link')
    ]

    return faculties
