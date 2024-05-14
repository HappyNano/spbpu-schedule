import math
import datetime
import typing as tp

import pytz
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from spbpu_schedule.database import database
from spbpu_schedule.parser import faculties, cource_groups
from spbpu_schedule.schedule import getapi as ga
import spbpu_schedule.storage.config as config


db = database.Database()

faculties_arr = faculties.get(config.FACULTIES_URL)
cource_groups_arr = [
    cource_groups.get(config.FACULTIES_URL + faculty.href) for faculty in faculties_arr
]

bot = telebot.TeleBot(config.BOT_KEY)


def gen_list_markup(arr: tp.List[tp.Any], name: str, page: int = 0, page_size: int = 4):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    i = page * page_size
    for index in range(i, min(i + page_size, len(arr))):
        markup.add(InlineKeyboardButton(arr[index], callback_data=f"{name}_{index}"))
    left_page = max(0, page - 1)
    right_page = min(math.ceil(len(arr) / page_size) - 1, page + 1)
    if len(arr) != page_size:
        markup.row(
            InlineKeyboardButton("⬅️" if left_page != page else "❌", callback_data=f"{name}_page{-1 if left_page == page else left_page}"),
            InlineKeyboardButton("➡️" if right_page != page else "❌", callback_data=f"{name}_page{-1 if right_page == page else right_page}")
        )
    return markup


def generate_days_markup(page=1):
    day = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    day = day if day.isoweekday() < 4 else day + datetime.timedelta(days=7)
    day -= datetime.timedelta(days=day.isoweekday() - 1)
    days_arr = []
    for week_i in range(-1, 3):
        days_arr += [(wd + ". " + (day + datetime.timedelta(days=i, weeks=week_i)).strftime('%d %B, %Y') ) for i, wd in enumerate(["Пн", "Вт", "Ср", "Чт", "Пт", "Сб"])]
    today_weekday = datetime.datetime.today().isoweekday()
    if today_weekday < 7:
        days_arr[6 + today_weekday - 1] += ' ' + "📌"
    return gen_list_markup(days_arr, "sw", page=page, page_size = 6)


@bot.callback_query_handler(func=lambda call: call.data.startswith("fc"))
def callback_query_fc(call):
    value: str = call.data[3:]
    if value.startswith("page"):
        page: int = int(value[4:])
        if page == -1:
            bot.answer_callback_query(call.id, "End")
            return
        faculties_names: tp.List[str] = list(map(lambda x: x.name, faculties_arr))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_list_markup(faculties_names, "fc", page)
        )
    else:
        course_names: tp.List[str] = list(map(lambda x: x.name, cource_groups_arr[int(value)]))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_list_markup(course_names, f"cs_{value}", page_size = len(course_names))
        )


@bot.callback_query_handler(func=lambda call: call.data.startswith("cs"))
def callback_query_cs(call):
    values = list(map(int, call.data[3:].split('_')))
    group_names: tp.List[str] = list(map(lambda x: x.name, cource_groups_arr[values[0]][values[1]].groups))
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=gen_list_markup(group_names, f"gr_{values[0]}_{values[1]}", page_size=6)
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("gr"))
def callback_query_gr(call):
    values = call.data[3:].split('_')
    if values[2].startswith("page"):
        page: int = int(values[2][4:])
        if page == -1:
            bot.answer_callback_query(call.id, "End")
            return
        group_names: List[str] = list(map(lambda x: x.name, cource_groups_arr[int(values[0])][int(values[1])].groups))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_list_markup(group_names, f"gr_{int(values[0])}_{int(values[1])}", page, page_size=6)
        )
    else:
        group_key = cource_groups_arr[int(values[0])][int(values[1])].groups[int(values[2])].key
        group_name = cource_groups_arr[int(values[0])][int(values[1])].groups[int(values[2])].name
        db.add_user(call.message.chat.id, group_key)
        bot.send_message(chat_id=call.message.chat.id, text=f"Твоя группа - {group_name}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("sw"))
def callback_query_sw(call):
    value = call.data[3:]
    if value.startswith("page"):
        page: int = int(value[4:])
        if page == -1:
            bot.answer_callback_query(call.id, "End")
            return
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выбери день:",
            reply_markup=generate_days_markup(page),
            parse_mode='HTML'
        )
        return
    if value == "back":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выбери день:",
            reply_markup=generate_days_markup(),
            parse_mode='HTML'
        )
        return

    group_key = db.get_group_id(user_id=call.message.chat.id)
    result = ga.get(f'на неделю {int(value) // 6 - 1}', group_key)
    result: str = result[int(value) % 6]

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Назад", callback_data="sw_back"))
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=result if len(result) != 0 else "Отдых!",
        reply_markup=markup,
        parse_mode='HTML'
    )


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    faculties_names: tp.List[str] = list(map(lambda x: x.name, faculties_arr))
    bot.reply_to(message, "Привет, выбери группу:", reply_markup=gen_list_markup(faculties_names, "fc"))


@bot.message_handler(commands=['schedule'])
def send_schedule(message):
    group_key = db.get_group_id(user_id=message.chat.id)
    if group_key is None:
        bot.reply_to(message, "Выбери группу!")
        return

    result: str = ga.get('на сегодня', group_key)[0]
    bot.reply_to(message, result if len(result) != 0 else "Отдых!", parse_mode='HTML')


@bot.message_handler(commands=['schedule_week'])
def send_schedule_week(message):
    group_key = db.get_group_id(user_id=message.chat.id)
    if group_key is None:
        bot.reply_to(message, "Выбери группу!")
        return
    bot.reply_to(
        message, "Выбери день:",
        reply_markup=generate_days_markup(),
        parse_mode='HTML'
    )


bot.infinity_polling()
