#import os
#import csv
#import sqlite3
#import requests
#from datetime import datetime

# функция регистрации пользователя. iD = message.chat.id
async def statId(iD, c):
    cur = c.cursor()
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """SELECT count() status FROM sessions WHERE ChatId = ?""", (iD,)
            )
            if cur.fetchone()[0] == 0:
                cur.close()
                return False
            else:
                cur.close()
                return True
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция проверки состояния меню. iD = message.chat.id
async def MenuInfo(iD, c):
    cur = c.cursor()
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT Menu FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            return row[0]
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

# функция возврата записи . iD = message.chat.id
async def recordInfo(iD, c):
    cur = c.cursor()
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT * FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            return row
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

# функция записи пользоватьеля в базу данных. chat = message.chat
async def recordChat(chat_in, c):
    noww = datetime.now()
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """DELETE FROM sessions WHERE Menu <> 0 AND ChatId = ?;""",
                (chat_in.id,),
            )
            data_in = (
                chat_in.id,
                chat_in.first_name,
                chat_in.last_name,
                chat_in.username,
                noww,
                False,
                100,
            )
            cur.execute(
                """INSERT INTO sessions (ChatId, Firstname, Lastname, usermame, DateTimeSessy, Status, Menu) VALUES (?, ?, ?, ?, ?, ?, ? );""",
                data_in,
            )
            c.commit()
            cur.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция записи номера автомобиля, состояния меню. iD = message.chat.id
async def сomUpd(iD, comment_db, c):
    cur = c.cursor()
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """UPDATE sessions set Comment = ?, Menu = ? WHERE ChatId = ?""",
                (
                    comment_db,
                    50,
                    iD,
                ),
            )
            c.commit()
            cur.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция записи телефона, состояния меню. iD = message.chat.id
async def phoneUpd(iD, comment_db, c):
    cur = c.cursor()
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """UPDATE sessions set phone = ?, Menu = ? WHERE ChatId = ?""",
                (
                    comment_db,
                    0,
                    iD,
                ),
            )
            c.commit()
            cur.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция записи строки в csv-файл
async def csvUpd(infoz, pathz):
    noww = datetime.now()
    filez = pathz + 'журнал-' + noww.strftime("%Y-%m-%d") + '.csv'
    try:
        fe = os.path.isfile(filez)
        zFile = open(filez, 'a', newline='')
        # zFile = open(filez, 'a', encoding='utf-8', newline='')
        with zFile:
            writer = csv.writer(zFile, delimiter = ';')
            if not fe:
                zHeader = [["Дата-время", "Направление", "Идентификатор", "Ник"]]
                writer.writerows(zHeader)
            writer.writerows(infoz)
            zFile.close()
            print("Запись произведена")
    except FileNotFoundError:
        print("Ошибка записи в файл.")


# ChatId
# Firstname
# Firstname
# username
# DateTimeSessy
# Status
# Menu
# Comment
# phone
# "id": 1352204347