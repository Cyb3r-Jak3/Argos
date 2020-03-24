import sqlite3
import csv
import os
from datetime import datetime

CONNECTION = sqlite3.connect("cowrie.db")
CURSOR = CONNECTION.cursor()

NOW = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")

directory = f"reports-{NOW}"
os.mkdir(directory)


def fetch(table: str):
    "Returns a table of results"
    # The select is bad pratice
    # Unfortunately, tables can't be the target of parameter substitution
    format_str = f"SELECT * FROM {table};"  # nosec
    CURSOR.execute(format_str)
    fetched = CURSOR.fetchall()
    return fetched


def table_to_csv(table: str, items: list):
    with open(f"{directory}/{table}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(items)
        for entry in fetch(table):
            writer.writerow(entry)


if __name__ == "__main__":
    table_to_csv("auth", ["ID", "Session", "Success",
                          "Username", "Password", "Timestamp"])
    table_to_csv("clients", ["ID", "Version"])
    table_to_csv("input", ["ID", "Session", "Timestamp",
                           "Realm", "Success", "Input"])
    table_to_csv("sensors", ["ID", "IP"])
    table_to_csv("sessions", ["ID", "Start Time", "End Time",
                              "Sensor", "IP", "Termsize", "Client"])
    table_to_csv("ttylog", ["ID", "Session", "ttylog", "size"])
    table_to_csv("downloads", ["ID", "Session", "Timestamp",
                               "url", "outfile", "shasum"])
    table_to_csv("keyfingerprints",
                 ["ID", "Session", "Username", "Fingerprint"])
    table_to_csv("params", ["ID", "Session", "Arch"])
    table_to_csv("ipforwardsdata", ["ID", "Session", "Timestamp",
                                    "DST IP", "DST Port", "Data"])
    print(NOW)
