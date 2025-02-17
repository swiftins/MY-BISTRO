import telebot
from telebot import types
from order_manager import FoodOrderManager
from db_module import DBConnector, DBManager
import uuid
from design import create_reply_kbd, create_inline_kbd

# Показать главное меню
def show_main_menu(bot,message,user_data):

    main_menu = ["Меню","Мои заказы", "Отзывы", "Выйти"]
    keyboard = create_reply_kbd(row_width=2, values=main_menu, back = None)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step" : "Main_menu"}

def show_menu_categories(bot,message,categories,user_data):
    category = [row[1] for row in categories]
    keyboard = create_reply_kbd(row_width=3, values=category, back="Назад")
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step" : "Categories_menu"}

def show_menu_category_items(bot,message,items,user_data):
    item = [f"{row[2]} - {row[4]} руб." for row in items]
    keyboard = create_reply_kbd(row_width=3, values=item, back="Назад")
    bot.send_message(message.chat.id, "Выберите блюдо:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step": "Items_menu"}