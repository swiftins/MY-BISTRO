import telebot
from telebot import types
import os

TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'
bot = telebot.TeleBot(TOKEN)

def create_tile_kbd(keyboard=None,rows=3,cols=3, msg=["",""], splitter="",btntype=types.KeyboardButton ):
    for i in range(rows):
        btns = []
        for j in range(cols):
            btns.append(btntype(f"{msg[0]}{splitter}{(i+1)*(j+1)}{splitter}{msg[1]}"))
        keyboard.row(*btns)

def create_tile_inline_kbd(keyboard=None,rows=3,cols=3, msg=""):
    for i in range(rows):
        btns = []
        for j in range(cols):
            btns.append(types.InlineKeyboardButton(f"{(i+1)*(j+1)}"))
        keyboard.row(*btns)



# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    image_path = os.path.join('img', 'zap_brok.jpg')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=9)

    # Добавляем кнопки в 3 ряда по 3 кнопки
    # for i in range(3):
    #     btns = []
    #     for j in range(3):
    #         btns.append(types.KeyboardButton(f"Кнопка {(i+1)*(j+1)}"))
    #     keyboard.row(*btns)
    create_tile_kbd(keyboard,msg=["Категория ",""])



    image_kbd = types.InlineKeyboardMarkup(row_width=3)
    # button = types.InlineKeyboardButton(text="Подробнее", url="https://example.com")
    # image_kbd.add(button)
    create_tile_kbd(image_kbd,msg=["",'шт.'])
    # Отправляем локальное фото с кнопкой
    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id,
                       photo=photo,
                       caption="Это локальное изображение с набором кнопок",
                       reply_markup=image_kbd)

    bot.send_message(message.chat.id, "Выбери кнопку:", reply_markup=keyboard)


# Запуск бота
bot.infinity_polling()