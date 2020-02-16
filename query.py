#!/usr/bin/env python3

import sqlite3
from datetime import datetime

connection = sqlite3.connect("cowrie.db")
cursor = connection.cursor()

now = datetime.now()
now.strftime("%d/%m/%Y %H:%M:%S")


def fetch(table: str):
    "Returns a table of results"
    format_str = """SELECT * FROM %s);"""
    cursor.execute(format_str, (table))
    fetched = cursor.fetchall()
    return fetched


tables = ["auth", "clients", "input",
          "sensors", "sessions", "ttylog",
          "downloads", "keyfingerprints"]

for table in tables:
    print(fetch(table))
