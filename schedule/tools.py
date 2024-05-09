import json
import asyncio
import httpx

from config import config

def getData(url: str) -> json:
    with httpx.Client() as client:
        return (client.get(url=url)).json()

def is_groupId_correct(group_id: int) -> bool:
    try:
        url = config.SCHEDULE_URL.format(group_id)
        data = getData(url)
        return data['error'] is None
    except:
        return True
