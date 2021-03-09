import psycopg2
from psycopg2 import sql

import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')


class Postgres:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=config.get('postgres', 'dbname'), user=config.get('postgres', 'user'),
                                     password=config.get('postgres', 'password'),
                                     host=config.get('postgres', 'host'))
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def close(self):
        self.cursor.close()
        self.conn.close()

    def add_post(self, text: str, vk_id: int):
        values = [(text, vk_id), ]
        stmt = sql.SQL('insert into post (text, vk_id) values {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        self.cursor.execute(stmt)

    def is_post_in(self, vk_id):
        self.cursor.execute('''select * from post where vk_id={}'''.format(vk_id))
        if self.cursor.fetchone():
            return True
        return False

    def truncate_table(self, name):
        self.cursor.execute('truncate {}'.format(name))

    def get_posts_text(self) -> list:
        text = []
        columns = ('text',)
        stmt = sql.SQL('SELECT {} FROM {}').format(
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.Identifier('post')
        )
        self.cursor.execute(stmt)

        for row in self.cursor:
            text.append(row)

        return text

    def save_words(self, words: list):
        stmt = sql.SQL('insert into word (name, count) values {}').format(
            sql.SQL(',').join(map(sql.Literal, words))
        )
        self.cursor.execute(stmt)
