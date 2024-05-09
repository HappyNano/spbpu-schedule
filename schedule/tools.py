import json
import asyncio
import httpx

from config import config

def getData(url: str) -> json:
    with httpx.Client() as client:
        return (client.get(url=url)).json()

def is_groupId_correct(group_id: int) -> bool:
    loop = asyncio.get_event_loop()
    try:
        url = config.SCHEDULE_URL.format(group_id)
        data = loop.run_until_complete(asyncio.gather(getData(url)))[0]
        return data['error'] is None
    except:
        return True

def is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except:
        return False