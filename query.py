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


def auth_table():
    with open(f"{directory}/auth.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Success",
                         "Username", "Password", "Timestamp"])
        for entry in fetch("auth"):
            writer.writerow(entry)


def client_table():
    with open(f"{directory}/clients.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Version"])
        for entry in fetch("clients"):
            writer.writerow(entry)


def input_table():
    with open(f"{directory}/input.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Timestamp",
                         "Realm", "Success", "Input"])
        for entry in fetch("input"):
            writer.writerow(entry)


def sensors_table():
    with open(f"{directory}/senors.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "IP"])
        for entry in fetch("sensors"):
            writer.writerow(entry)


def sessions_table():
    with open(f"{directory}/sessions.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Start Time", "End Time",
                         "Sensor", "IP", "Termsize", "Client"])
        for entry in fetch("sessions"):
            writer.writerow(entry)


def ttylog_table():
    with open(f"{directory}/ttylog.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "ttylog", "size"])
        for entry in fetch("ttylog"):
            writer.writerow(entry)


def downloads_table():
    with open(f"{directory}/downloads.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Timestamp",
                         "url", "outfile", "shasum"])
        for entry in fetch("downloads"):
            writer.writerow(entry)


def keyfingerprints_table():
    with open(f"{directory}/keyfingerprints.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Username", "Fingerprint"])
        for entry in fetch("keyfingerprints"):
            writer.writerow(entry)


def params_table():
    with open(f"{directory}/params.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Arch"])
        for entry in fetch("params"):
            writer.writerow(entry)


def ipforwardsdata_table():
    with open(f"{directory}/ipforwardsdata.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Session", "Timestamp",
                         "DST IP", "DST Port", "Data"])
        for entry in fetch("ipforwardsdata"):
            writer.writerow(entry)


if __name__ == "__main__":
    auth_table()
    client_table()
    input_table()
    sensors_table()
    sessions_table()
    ttylog_table()
    downloads_table()
    keyfingerprints_table()
    params_table()
    ipforwardsdata_table()
    print(NOW)
