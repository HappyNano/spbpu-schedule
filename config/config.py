# Database
DATABASE_NAME = 'schedule'
DATABASE_USER = 'admin'
DATABASE_PASS = 'admin'
DATABASE_HOST = '192.168.0.110'
DATABASE_TABLE_NAME = 'users_group'

# Urls
FACULTIES_URL = 'https://ruz.spbstu.ru/'
SCHEDULE_URL = 'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{}?date='

# В файле tg.key хранится только ключ от telegram-бота
BOT_KEY = ""
with open('tg.key', 'r') as file:
    BOT_KEY = file.readline()