#!/usr/bin/env python3

import sqlite3


class SQLite:

    def __init__(self):
        self.conn = sqlite3.connect('sbrt.db')
        self.c = self.conn.cursor()

    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS sbrt
                     (message_type text,
                     contact_name text,
                     readable_date text,
                     read text,
                     date real,
                     address text,
                     body text,
                     type text)''')

    def insert_row(self, message):
        message_type = message.tag
        message = message.attrib
        self.c.execute("INSERT INTO sbrt VALUES (?,?,?,?,?,?,?,?)", [
            message_type,
            message['contact_name'],
            message['readable_date'],
            message['read'],
            message['date'],
            message['address'],
            message['body'],
            message['type']
        ])

    def commit_db(self):
        self.conn.commit()
