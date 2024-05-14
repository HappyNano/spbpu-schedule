import psycopg2
from spbpu_schedule.storage import config

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=config.DATABASE_NAME,
            user=config.DATABASE_USER,
            password=config.DATABASE_PASS,
            host=config.DATABASE_HOST
        )
        self.cur = self.conn.cursor()

    def add_user(self, user_id, group_id):
        print(user_id, group_id)
        self.__execute_query(f"""INSERT INTO {config.DATABASE_TABLE_NAME} (user_id, group_id)
VALUES ({user_id}, {group_id})
ON CONFLICT (user_id) DO UPDATE
SET user_id = excluded.user_id,
    group_id = excluded.group_id;""")
        self.conn.commit()

    def get_group_id(self, user_id):
        self.__execute_query(f"SELECT group_id FROM {config.DATABASE_TABLE_NAME} WHERE user_id={user_id};")
        res = self.cur.fetchone()
        self.conn.commit()
        if res is None:
            return None
        return res[0]

    def __execute_query(self, query):
        self.cur.execute(query)
