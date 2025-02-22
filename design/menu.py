import telebot
from telebot import types
import threading
import os
from order_manager import FoodOrderManager
from db_module import DBConnector, DBManager
import uuid
from order_manager import FoodOrderManager, init_fo_manager
from design import create_reply_kbd, create_inline_kbd
from payment import process_payment_animation


# Показать главное меню
def show_main_menu(bot,message,user_data):
    user_id = message.from_user.id
    main_menu = ["Меню","Мои заказы", "Отзывы", "Оформить заказ", "Почистить чат","Выйти"]
    keyboard = create_reply_kbd(row_width=2, values=main_menu, back = None)
    msg = bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)
    print(user_data)
    user_data[user_id]["step"]= "Main_menu"
    return msg.chat.id, msg.message_id

def show_menu_categories(bot,message,categories,user_data):
    user_id = message.from_user.id
    category = [row[1] for row in categories]
    category.append("Оформить заказ")

    print(message.chat.id)
    keyboard = create_reply_kbd(row_width=3, values=category, back="Назад")
    msg = bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=keyboard)
    user_data[user_id]["step"] = "Category_menu"
    return msg.chat.id, msg.message_id

def show_menu_category_items(bot,message,items,user_data):
    user_id = message.from_user.id
    item = [f"{row[2]} - {row[4]} руб." for row in items]
    item.append("Оформить заказ")
    keyboard = create_reply_kbd(row_width=3, values=item, back="Назад")
    msg = bot.send_message(message.chat.id, "Выберите блюдо:", reply_markup=keyboard)
    user_data[user_id].update( {"step": "Item_menu", "category": items[0][1]})
    return msg.chat.id, msg.message_id

def select_quantity(bot,message,item_name,image_path=None,number_of_seats = 8,msg = ["",""]):
    user_id = message.from_user.id
    keyboard = create_inline_kbd(row_width=4,nums=number_of_seats,msg=msg)
    if image_path is not None:
        if not os.path.exists(image_path):#and os.path.isfile(file_path):
            image_path = os.path.join('img', 'empty.jpg')
        with open(image_path, 'rb') as photo:
            msg = bot.send_photo(message.chat.id,
                           photo=photo,
                           caption=f"{item_name} ",
                           reply_markup=keyboard,
                           parse_mode = 'HTML'
            )
        return msg.chat.id, msg.message_id


    #bot.send_message(message.chat.id, "Выберите количество:", reply_markup=keyboard)


def make_menu_categories(bot,message,user_data):
    food_order_manager = init_fo_manager()
    categories = food_order_manager.get_menu_categories()
    msg = show_menu_categories(bot,message,categories,user_data)
    food_order_manager.db_manager.close()
    return msg

def make_menu_category_items(bot,message,user_data):
    food_order_manager = init_fo_manager()
    category_name = message.text
    if category_name == "Назад":
        make_menu_categories(bot, message, user_data)
        return
    category_id = next(
        category[0] for category in food_order_manager.get_menu_categories() if category[1] == category_name)
    items = food_order_manager.get_menu_items(category_id=category_id)

    msg = show_menu_category_items(bot, message, items, user_data)
    food_order_manager.db_manager.close()
    bot.delete_message(message.chat.id, message.message_id)
    return msg

def make_quantity_dialog(bot,message,user_data):
    food_order_manager = init_fo_manager()
    user_id = message.from_user.id
    item_name = message.text.split(' - ')[0]
    item_info = food_order_manager.get_menu_item_id_by_name(item_name)[0]
    item_id=item_info[0]
    item_category = food_order_manager.get_menu_categories(item_info[1])[0][1]
    item_caption = f"<u><b>{item_name}</b> - {item_info[4]} руб.</u>\n{item_info[3]}"
    user_data[user_id].update({
        'selected_item' : item_name,
        "step":"Item_quantity",
        "item_id":item_id,
        "category":item_category[2:-1],
    })
    folder=(user_data[user_id]["category"].split(" ")[0]).lower()
    file="_".join(user_data[user_id]["selected_item"].split(" "))+".jpg"
    print(user_data)
    image_path = os.path.join('img', folder, file)
    user_data[user_id]["old_message"] = select_quantity(bot, message, item_caption, image_path=image_path,  msg=["","шт."])
    bot.delete_message(message.chat.id, message.message_id)

def show_order(bot,message,user_data):
    food_order_manager = init_fo_manager()


def show_help(bot,message,user_data):
    help_text = (
        "🍽 *Добро пожаловать в помощник ресторана!*\n\n"
        "*Основные команды:*\n"
        "• /start - Начать работу с ботом\n"
        "• /help - Вывод справочной информации\n"

        "*Как сделать заказ:*\n"
        "1. Выберите 'Меню' или используйте Меню\n"
        "2. Выберите категорию блюд\n"
        "3. Выберите блюдо и укажите количество\n"
        "4. Выберите из меню 'Оформить заказ'\n"
        "5. Проверьте корректность заказа или откорректируйте его\n"
        "6. Оплатите или вернитесь к добавлению блюд в заказ\n\n"

        "*Дополнительные возможности:*\n"
        "• Просмотр описания и фото блюд\n"
        "• Изменение количества порций\n"
        "• Отслеживание статуса заказа\n"
        "• Просмотр истории заказов\n"
        "• Система отзывов\n\n"

        "Если у вас возникли вопросы или проблемы, пожалуйста, свяжитесь с нашей поддержкой."
    )

    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
    bot.delete_message(message.chat.id, message.message_id)

def show_feedback(bot,message,user_data):
    bot.delete_message(message.chat.id, message.message_id)
    text = "Мы уже тестируем <b>суперсекретный</b> алгоритм обработки отзывов... 🍕🤖 Пока он учится различать «вкусно» и «очень вкусно», оставайтесь с нами! Скоро запустим! 🚀"
    bot.send_message(message.chat.id, text, parse_mode='HTML')


def show_pay_form(bot,message,user_data):
    user_id = message.from_user.id
    keyboard = create_inline_kbd(row_width=2, nums=3, values=["💳Картой 💳","💵 Наличными 💵", "📱 Мобильная оплата 📱"], keys=['Назад',"pay_card","pay_cache","pay_mobile"] )
    image_path = r"img\pay_method.png"
    if not os.path.exists(image_path):  # and os.path.isfile(file_path):
        image_path = os.path.join('img', 'empty.jpg')
    with open(image_path, 'rb') as photo:
        msg = bot.send_photo(message.chat.id,
                             photo=photo,
                             caption=f"💰      Способ оплаты      💰",
                             reply_markup=keyboard,
                             parse_mode='HTML'
                             )
    return msg.chat.id, msg.message_id


def online_pay(bot,message,user_data):
    user_id = message.chat.id
    order_id = user_data[user_id]["order_id"]
    order = user_data[user_id]["pay_order"]
    # bot.delete_message(call.message.chat.id, call.message.message_id)
    threading.Thread(
        target=process_payment_animation,
        args=(bot,
              message,
              order[1],
              order[3],
              order[2],
              order_id,
              user_data
              )
    ).start()
