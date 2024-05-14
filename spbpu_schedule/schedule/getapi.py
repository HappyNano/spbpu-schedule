import datetime
import json
import typing as tp

import pytz

from spbpu_schedule.storage import config
from spbpu_schedule.schedule.tools import getData

def parse_subject(subject: json) -> str:
    subj = f"{subject['typeObj']['name']}"
    subj = ("&#x1f4d6" if subj.startswith("Лекц") else "&#x1f4dd") + " " + subj
    result = f"&#x1f559 {subject['time_start']} - {subject['time_end']}\n&#x1f3f7 {subject['subject']}\n{subj}\n"
    
    teachers = subject['teachers']
    if teachers is not None:
        for teacher in teachers:
            result += "&#x1f9d1&#x200d&#x1f3eb " + teacher['full_name'] + '\n'
    auditories = subject['auditories']

    if auditories is not None:
        for auditory in auditories:
            audty = f"{auditory['name']}, {auditory['building']['name']}\n"
            audty = ("&#x1f4bb" if audty.startswith("Дист") else "&#x1f6b6") + " " + audty
            result += audty
    return result


def parse_day(day: json) -> str:
    result = ""
    for subject in day['lessons']:
        result += parse_subject(subject) + '\n'
    return result


def get(action: str, group_id: int) -> tp.List[str]:
    today = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    transform_action = {
        'на сегодня': today,
        'на завтра': today + datetime.timedelta(days=1),
        'на неделю': today if today.isoweekday() < 4 else today + datetime.timedelta(days=7),
    }
    try:
        if action.startswith('на неделю '):
            date: datetime = today + datetime.timedelta(weeks=int(action[10:]))
        else: 
            date: datetime = transform_action[action]
    except:
        return "error"
    
    schedule = getData(config.SCHEDULE_URL.format(group_id) + date.strftime('%Y-%m-%d'))

    week: list = schedule['days']
    
    transform_day_number = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье',
    }

    msg = []
    msg_text = ""
    if action == 'на сегодня' or action == 'на завтра':
        for day in week:
            is_today = day['weekday'] == today.isoweekday() and action == 'на сегодня'
            is_tomorrow = day['weekday'] == (today.isoweekday() + 1) % 7 and action == 'на завтра'
            if is_today or is_tomorrow:
                msg_text += f"&#x1f5d3 <b>{day['date']} ({transform_day_number[day['weekday']]})</b>\n\n"
                msg_text += parse_day(day)
                msg.append(msg_text)
                msg_text = ""
    else:
        d: int = 1
        for day in week:
            while day['weekday'] != d and d < 8:
                msg.append("")
                d += 1
            d += 1
            msg_text += f"&#x1f5d3 <b>{day['date']} ({transform_day_number[day['weekday']]})</b>\n\n"
            msg_text += parse_day(day) + '\n'
            msg.append(msg_text)
            msg_text = ""

    return msg
