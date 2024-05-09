import math, datetime, pytz

from typing import List, Any

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import config.config as config
from parser import faculties, cource_groups

import schedule.getapi as ga

faculties_arr = faculties.get()
cource_groups_arr = list(map(lambda x: cource_groups.get(x.href), faculties_arr))

bot = telebot.TeleBot(config.BOT_KEY)

def gen_list_markup(arr: List[Any], name: str, page: int = 0, page_size: int = 4):
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

@bot.callback_query_handler(func=lambda call: call.data.startswith("fc"))
def callback_query_fc(call):
    value: str = call.data[3:]
    if value.startswith("page"):
        page: int = int(value[4:])
        if page == -1:
            bot.answer_callback_query(call.id, "End")
            return
        faculties_names: List[str] = list(map(lambda x: x.name, faculties_arr))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_list_markup(faculties_names, "fc", page)
        )
    else:
        course_names: List[str] = list(map(lambda x: x.name, cource_groups_arr[int(value)]))
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=gen_list_markup(course_names, f"cs_{value}", page_size = len(course_names))
        )

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    faculties_names: List[str] = list(map(lambda x: x.name, faculties_arr))
    bot.reply_to(message, "Привет, выбери группу:", reply_markup=gen_list_markup(faculties_names, "fc"))

bot.infinity_polling()
