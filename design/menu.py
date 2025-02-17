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
    pass

def show_menu_categories(bot,message,categories,user_data):
    category = [row[1] for row in categories]
    keyboard = create_reply_kbd(row_width=3, values=category, back="Назад")
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step" : "Category_menu"}
    pass

def show_menu_category_items(bot,message,items,user_data):
    item = [f"{row[2]} - {row[4]} руб." for row in items]
    keyboard = create_reply_kbd(row_width=3, values=item, back="Назад")
    bot.send_message(message.chat.id, "Выберите блюдо:", reply_markup=keyboard)
    user_data[message.from_user.id] = {"step": "Item_menu", "category": items[0][1]}
    pass

def select_quantity(bot,message,item_name,image_path=None,number_of_seats = 8):
    keyboard = create_inline_kbd(row_width=4,nums=number_of_seats)
    if image_path is not None:
        with open(image_path, 'rb') as photo:
            bot.send_photo(message.chat.id,
                           photo=photo,
                           caption=f"Это изображение блюда {item_name} набором кнопок",
                           reply_markup=keyboard)


    bot.send_message(message.chat.id, "Выберите количество:", reply_markup=keyboard)
