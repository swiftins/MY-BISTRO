import telebot
from telebot import types
from order_manager import FoodOrderManager
from db_module import DBConnector, DBManager
import uuid
from design import create_reply_kbd, create_inline_kbd

# Показать главное меню
def show_main_menu(bot,chat_id):

    main_menu = ["Меню","Мои заказы", "Отзывы", "Выйти"]
    keyboard = create_reply_kbd(row_width=2, values=main_menu, back = None)
    # markup = types.ReplyKeyboardMarkup(row_width=2)
    # btn_menu = types.KeyboardButton('Меню')
    # btn_orders = types.KeyboardButton('Мои заказы')
    # markup.add(btn_menu, btn_orders)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=keyboard)
