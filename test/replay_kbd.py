from math import floor, ceil
import telebot
from telebot import types

import os

from telebot.types import InlineKeyboardButton

TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'
bot = telebot.TeleBot(TOKEN)

# def create_tile_kbd(keyboard=None,rows=3,cols=3, msg=["",""], splitter="",btntype=types.KeyboardButton):
#     for i in range(rows):
#         btns = []
#         for j in range(cols):
#             btns.append(btntype(f"{msg[0]}{splitter}{(i+1)*(j+1)}{splitter}{msg[1]}"))
#         keyboard.row(*btns)
#
# def create_tile_inline_kbd(keyboard=None,rows=3,cols=3, msg=""):
#     for i in range(rows):
#         btns = []
#         for j in range(cols):
#             btns.append(types.InlineKeyboardButton(f"{(i+1)*(j+1)}"))
#         keyboard.row(*btns)
#

def create_tile_kbd(keyboard, row_width=1, nums=1, msg=["", ""], splitter="", values = None):
    """
    Универсальная функция для создания плиточной клавиатуры.
    Работает с ReplyKeyboardMarkup и InlineKeyboardMarkup.
    """
    if isinstance(keyboard, types.ReplyKeyboardMarkup):
        # Для обычных кнопок по умолчанию используем KeyboardButton
        btntype = types.KeyboardButton
    elif isinstance(keyboard, types.InlineKeyboardMarkup):
        # Для инлайн-кнопок используем InlineKeyboardButton
        btntype = types.InlineKeyboardButton
    else:
        raise TypeError("keyboard должен быть либо ReplyKeyboardMarkup, либо InlineKeyboardMarkup")

    # Создаем кнопки в виде плитки
    if values:
        if type(values) == list:
            values = [0,]+values
            nums = len(values)
        else:
            nums = 2
            values = [0,values]
    rows=ceil(nums/row_width)

    for i in range(rows):
        btns = []
        if (nums - (i+1)*row_width) >= 0:
            columns = row_width
        else:
            columns = nums % row_width

        for j in range(columns):
            val = (i) * row_width + j
            if val == 0:
                text = "X"
            elif type(values) == list:
                text = values[val]
            else:
                text = f"{msg[0]}{splitter}{val}{splitter}{msg[1]}"


            # Если это Inline кнопка, добавляем callback_data
            if btntype == types.InlineKeyboardButton:
                btns.append(btntype(text, callback_data=f"{val}"))
            else:
                btns.append(btntype(text))

        keyboard.row(*btns)

    return keyboard

def create_reply_kbd(row_width=2, values = []):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    create_tile_kbd(keyboard, row_width=row_width, msg=["Категория ", ""],values=values)
    return keyboard

def create_inline_kbd(row_width=3, nums=3, values = None):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    create_tile_kbd(keyboard, row_width=row_width, nums=nums, msg=["", ""], values=values)
    return keyboard


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    image_path = os.path.join('img', 'zap_brok.jpg')
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=9)
    #
    # create_tile_kbd(keyboard,msg=["Категория ",""])
    cat =["Завтраки","Салаты","Супы","Основные блюда","Десерты","Напитки"]
    keyboard = create_reply_kbd(row_width = 3,values=cat)


    image_kbd = types.InlineKeyboardMarkup(row_width=3)
    create_tile_kbd(image_kbd,msg=["",'шт.'])
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id,
                       photo=photo,
                       caption="Это локальное изображение с набором кнопок",
                       reply_markup=image_kbd)

    bot.send_message(message.chat.id, "Выбери кнопку:", reply_markup=keyboard)


# Запуск бота
bot.infinity_polling()