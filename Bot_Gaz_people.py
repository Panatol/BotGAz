
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import re
from config import *
# from deffer import *
# from defadmin import *
import csv
import sqlite3
# import requests
from datetime import datetime

# включить переменные среды для bat-файла
# bot = Bot(token=os.getenv('TOKEN'))

if __name__ == "__main__":
    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    db_filename = name_db
    conn = sqlite3.connect(db_filename)

@dp.message_handler(commands=["start", "help"])
async def start(message, res=False):
    if await statId(message.chat.id, conn):
        await on_Keyboard(message.chat.id, True)
    else:
        await on_Keyboard(message.chat.id, False)


@dp.message_handler(commands=["root"])
async def guru(message, res=False):
    await bot.send_message(message.chat.id, "Введите кодовое слово")


@dp.message_handler(content_types=["contact"])
async def contact(message):
    if message.contact is not None:
        global phonenumber
        phonenumber = str(message.contact.phone_number)
        # print(phonenumber)
        if await statId(message.chat.id, conn) == False:
            await recordChat(message.chat, conn)
        await phoneUpd(message.chat.id, phonenumber, conn)
        await bot.send_message(
            message.chat.id, " Для номера +" + phonenumber + "\nВведите номер лицевого счета,\nтолько цифры"
        )
    else:
        await bot.send_message(
            message.chat.id, "Регистрация без номера телефона невозможна"
        )

    await message.delete()

@dp.message_handler(text=["Команда голосом"])
async def vice_comm(message, res=False):
    if await BlockInfo(message.chat.id, conn):
        await bot.send_message(message.chat.id, "Обработка фразы. Скрипт в разработке")
    else:
        await bot.send_message(message.chat.id, text="Ваш контакт заблокирован,\nобратитесь к администратору", reply_markup=None)
    
    

@dp.message_handler(text=["Передать показания"])
async def start(message, res=False):
    if await BlockInfo(message.chat.id, conn):
        await bot.send_message(message.chat.id, "Передать показания. Скрипт в разработке")
    else:
        await bot.send_message(message.chat.id, text="Ваш контакт заблокирован,\nобратитесь к администратору", reply_markup=None)


@dp.message_handler(text=["Передать информацию"])
async def start(message, res=False):
    if await BlockInfo(message.chat.id, conn):
        await bot.send_message(message.chat.id, "Передать информацию. Скрипт в разработке")
    else:
        await bot.send_message(message.chat.id, text="Ваш контакт заблокирован,\nобратитесь к администратору", reply_markup=None)

@dp.message_handler()
async def defa(message, res=False):
    # пока только замена номера
    nom = await MenuInfo(message.chat.id, conn)
    if nom == 50:
        prvrk = re.match(r'\d{7}',message.text)
        if prvrk == None:
            await bot.send_message(message.chat.id, text="Ошибка!\nВведите цифры номера л/с\nВведите заново")
        else:
            await compUpd(message.chat.id, message.text, conn)
            await bot.send_message(message.chat.id, text="Регистрация завершена")
            await on_Keyboard(message.chat.id, True)
    elif nom == 40:
        # ветка заглушка для обработки ввода данных
        await bot.send_message(
            message.chat.id, text="В боте функция зарезервирована"
        )
        await message.delete()
    else:
        await bot.send_message(
            message.chat.id, text="В боте данное действие не обрабатывается"
        )
        await message.delete()


############################################### ФУНКЦИИ ###################################################################
async def on_startup(_):
    try:
        # conn = sqlite3.connect(db_filename)
        cur = conn.cursor()
        print("База данных SQLite успешно подключена")
        sqlite_select_query = "select sqlite_version();"
        cur.execute(sqlite_select_query)
        record = cur.fetchall()
        print("Версия базы данных SQLite: ", record)
        sqlite_select_query = "DELETE FROM sessions WHERE Menu <> 0;"
        cur.execute(sqlite_select_query)
        conn.commit()
        cur.close()
        print("Бот запущен")
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

async def on_Keyboard(Idd, n_variant):
    if await BlockInfo(Idd, conn):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        if  n_variant:   
                btn1 = types.KeyboardButton("Передать показания")
                btn2 = types.KeyboardButton("Передать информацию")
                btn3 = types.KeyboardButton("Команда голосом")
                markup.add(btn1, btn2, btn3)
        else:
                btn1 = types.KeyboardButton("Регистрация", request_contact=True)
                markup.add(btn1)
        await bot.send_message(Idd, text="Выберите кнопку", reply_markup=markup)
    else:
        await bot.send_message(Idd, text="Ваш контакт заблокирован,\nобратитесь к администратору", reply_markup=None)


# функция регистрации пользователя. iD = message.chat.id
async def statId(iD, c):
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
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT Menu FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            return row[0]
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция возврата номера телефона. iD = message.chat.id
async def PhoneInfo(iD, c):
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT phone FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            res = str(row[0])
            return res
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

# функция возврата Comment. iD = message.chat.id
async def CommentInfo(iD, c):
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT Comment FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            return row[0]
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)


# функция проверки блокировки контакта . iD = message.chat.id
async def BlockInfo(iD, c):
    try:
        with c:
            cur = c.cursor()
            cur.execute("SELECT Status FROM sessions WHERE ChatId = ?", (iD,))
            row = cur.fetchone()
            cur.close()
            if row == None:
                return True
            else:
                return row[0]
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)

# функция возврата записи . iD = message.chat.id
async def recordInfo(iD, c):
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
                regtype,
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


# функция записи номера лицевого счета, состояния меню. iD = message.chat.id
async def compUpd(iD, comment_db, c):
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """UPDATE sessions set Comment = ?, Menu = ? WHERE ChatId = ?""",
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


# функция записи телефона, состояния меню. iD = message.chat.id
async def phoneUpd(iD, comment_db, c):
    try:
        with c:
            cur = c.cursor()
            cur.execute(
                """UPDATE sessions set phone = ?, Menu = ? WHERE ChatId = ?""",
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


# функция записи строки в csv-файл
async def csvUpd(infoz, pathz):
    noww = datetime.now()
    filez = pathz + "журнал-" + noww.strftime("%Y-%m-%d") + ".csv"
    try:
        fe = os.path.isfile(filez)
        zFile = open(filez, "a", newline="")
        # zFile = open(filez, 'a', encoding='utf-8', newline='')
        with zFile:
            writer = csv.writer(zFile, delimiter=";")
            if not fe:
                zHeader = [["Дата-время", "Направление", "Идентификатор", "Ник телеграм", "Телефон", "Номер авто"]]
                writer.writerows(zHeader)
            writer.writerows(infoz)
            zFile.close()
            print("Запись в журнал " + filez +" произведена")
    except FileNotFoundError:
        print("Ошибка записи в файл.")


############################################### ФУНКЦИИ КОНЕЦ ###############################################################

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


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

    #nomX = re.match(r'\D\d{3}\D{2}\d{2}',comment_db)
    #if nomX == comment_db:
    #    print("Ошибка формата номера")