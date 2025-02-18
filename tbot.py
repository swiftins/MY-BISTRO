from types import SimpleNamespace
import telebot
from telebot import types

from order_manager import FoodOrderManager, init_fo_manager
from db_module import DBConnector, DBManager
import uuid
import os
import csv
from design import show_main_menu, show_menu_categories, show_menu_category_items, select_quantity
from design import (make_menu_categories,
                    make_menu_category_items,
                    make_quantity_dialog,
                    menu_tree_previous,
                    create_keyboard_variable_rows)

# Инициализация бота
TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'
#TOKEN = "7918967502:AAGbpGfUYbw0M5QphKGF0TR-8jnDYJsjEmw"
bot = telebot.TeleBot(TOKEN)

# Глобальная переменная для максимального количества порций
number_of_seats = 8  # Максимальное количество порций


# Инициализация менеджера заказов
# def init_fo_manager(db_type='sqlite'):
#     db_connector = DBConnector(db_type)
#     db_manager = DBManager(db_connector)
#     return FoodOrderManager(db_manager)

# Состояния для обработки заказов
sessions = {}
user_data = {}

def delete_old_message(message):
    user_id = message.from_user.id
    if (user_id in user_data
        and "old_message" in user_data[user_id]
        and user_data[user_id]["old_message"] is not None):
        bot.delete_message(message.chat.id, user_data[user_id]["old_message"])
        user_data[message.from_user.id]["old_message"] = None


# Инициирование события /start программно
def trigger_start(chat_id):
    # Создаем фейковое сообщение
    class FakeMessage:
        def __init__(self, message):
            self.chat = SimpleNamespace(id=message.chat.id)
            self.text = '/start'
            self.from_user = types.User(id= message.chat.id,
                                        is_bot=False,
                                        first_name=message.chat.first_name,
                                        last_name=message.chat.last_name,
                                        username=message.chat.username
                                        )

    # Вызываем обработчик как будто это сообщение от пользователя
    start(FakeMessage(chat_id))

# Команда старта
@bot.message_handler(commands=['start'])
def start(message):
    if hasattr(message, 'message_id'):
        bot.delete_message(message.chat.id, message.message_id)
    food_order_manager = init_fo_manager()
    user_id = message.from_user.id
    user_data[user_id]={}
    order_pending = food_order_manager.get_user_orders_by_status(user_id)[-1]
    if len(order_pending) > 0:
        user_data[user_id]['order_id'] = order_pending[0]
    user_data[user_id]["old_message"] = message


    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = f"{first_name or ''} {last_name or ''}"
    if full_name == " ":
        full_name = username
    # Проверка, существует ли пользователь
    if not food_order_manager.check_user_exists(telegram_id=user_id):
        if food_order_manager.create_user(user_id, username, first_name, last_name):
            bot.send_message(message.chat.id, f"😀 {full_name}, Вы успешно зарегистрированы!👍")
    else:
        bot.send_message(message.chat.id, f"👏С возвращением, {full_name} !🤗")

    # Отправка главного меню
    old_message = show_main_menu(bot,message,user_data)
    food_order_manager.db_manager.close()
    print(user_data)


# Показать меню
@bot.message_handler(func=lambda message: message.text == 'Меню')
def show_menu(message):
    bot.delete_message(message.chat.id, message.message_id)
    if message.from_user.id not in user_data:
        trigger_start(message)
        return
    #delete_old_message(message)
    user_data[message.from_user.id]["old_message"] = make_menu_categories(bot,message,user_data)
    bot.delete_message(message.chat.id, message.message_id)
    print(user_data)

# Показать блюда в категории
@bot.message_handler(func=lambda message: message.text in [category[1] for category in init_fo_manager().get_menu_categories()])
def show_category_items(message):
    bot.delete_message(message.chat.id, message.message_id)
    if len(user_data)==0:
        trigger_start(message)
        return False
    make_menu_category_items(bot, message, user_data)
    bot.delete_message(message.chat.id, message.message_id)
    # food_order_manager = init_fo_manager()
    # category_name = message.text
    # category_id = next(category[0] for category in food_order_manager.get_menu_categories() if category[1] == category_name)
    # items = food_order_manager.get_menu_items(category_id=category_id)
    # show_menu_category_items(bot,message,items, user_data)
    # food_order_manager.db_manager.close()

# Обработчик выбора блюда
@bot.message_handler(func=lambda message: message.text.endswith('руб.'))
def select_item_quantity(message):
    if len(user_data)==0:
        trigger_start(message)
        return False
    make_quantity_dialog(bot, message, user_data)

# Обработчик ввода количества
#@bot.message_handler(func=lambda message: message.text.endswith('шт.'))
@bot.message_handler(func=lambda message: message.text.isdigit() and 1<=int(message.text) <= number_of_seats)
def add_item_to_order(message):
    user_id = message.from_user.id
    quantity = int(message.text)
    print (user_data)

    if user_id not in user_data or 'selected_item' not in user_data[user_id]:
        bot.send_message(message.chat.id, "Ошибка: блюдо не выбрано.")
        return

    food_order_manager = init_fo_manager()
    item_name = user_data[user_id]['selected_item']
    item = next(item for item in food_order_manager.get_menu_items() if item[2] == item_name)

    # Создание заказа, если его еще нет
    if 'order_id' not in user_data[user_id]:
        order_id = str(uuid.uuid4())
        user_data[user_id]['order_id'] = order_id
        food_order_manager.create_order(user_id, total_price=0)

    # Добавление блюда в заказ
    food_order_manager.add_item_to_order(user_data[user_id]['order_id'], item[0], quantity)
    bot.send_message(message.chat.id, f"{quantity} порций '{item_name}' добавлено в заказ!")

    # Очищаем выбранное блюдо
    del user_data[user_id]['selected_item']

    # Возвращаем пользователя к выбору категорий и добавляем кнопку "Оформить заказ"
    show_menu_with_checkout(message.chat.id)
    food_order_manager.db_manager.close()

# Показать меню с кнопкой "Оформить заказ"
def show_menu_with_checkout(chat_id):
    food_order_manager = init_fo_manager()
    categories = food_order_manager.get_menu_categories()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for category in categories:
        markup.add(types.KeyboardButton(category[1]))
    markup.add(types.KeyboardButton('Оформить заказ'))
    markup.add(types.KeyboardButton('Назад'))
    bot.send_message(chat_id, "Выберите категорию или оформите заказ:", reply_markup=markup)
    food_order_manager.db_manager.close()


# Обработчик оформления заказа
@bot.message_handler(func=lambda message: message.text == 'Оформить заказ')
def checkout_order(message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    user_id = message.from_user.id
    print(f"{user_id} - Нажал 'Оформить заказ'")
    food_order_manager = init_fo_manager()
    user_data[user_id] = user_data.get(user_id, {})
    msg = None
    if 'order_id' not in user_data[user_id]:
        order_pending = food_order_manager.get_user_orders_by_status(user_id)[-1]
        if len(order_pending) > 0:
            user_data[user_id]['order_id'] = order_pending[0]
            msg = bot.send_message(chat_id, "Найден заказ.")
        else:
            msg.bot.send_message(chat_id, "Ваш заказ пуст.")
            return


    order_id = user_data[user_id]['order_id']

    # Получаем информацию о заказе
    order_items = food_order_manager.get_order_items(order_id)
    if len(order_items) == 0:
        bot.send_message(chat_id, "Ваш заказ пуст.")
        return
    total_price = sum(item[2] * item[3] for item in order_items)  # price * quantity
    title = f"<b>Ваш заказ</b> :  {total_price} руб."
    # Формируем инлайн-клавиатуру с заказом
    kbd = create_keyboard_variable_rows(order_items)
    user_data[user_id]["order_form"] = bot.send_message(chat_id, title, reply_markup=kbd, parse_mode='HTML')
    # Возвращаем пользователя в главное меню
    show_main_menu(bot,message,user_data)
    food_order_manager.db_manager.close()
    if msg:
        bot.delete_message(message.chat.id, msg.message_id)


@bot.message_handler(func=lambda message: message.text == "Почистить чат")
def clear_chat(message):
    chat_id = message.chat.id

    # Получаем последние 10 сообщений в чате
    message_ids = [message.message_id - i for i in range(100)]

    # Пытаемся удалить каждое сообщение
    for msg_id in message_ids:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение с ID {msg_id}: {e}")

@bot.message_handler(func=lambda message: message.text == 'X' or message.text == 'Назад' or message.text == '0' or message.text == '❌')
def go_back(message):
    if len(user_data)==0:
        trigger_start(message)
        return False
    print(user_data)
    usr_data = user_data[message.from_user.id]
    #previous_step = menu_tree_previous[usr_data["step"]][0]
    previous_menu = menu_tree_previous[usr_data["step"]][1]
    previous_menu(bot, message, user_data)
    bot.delete_message(message.chat.id, message.message_id)

# Показать заказы пользователя
@bot.message_handler(func=lambda message: message.text == 'Мои заказы')
def show_user_orders(message):
    food_order_manager = init_fo_manager()
    user_id = message.from_user.id
    print(f"{user_id} - Нажал 'Мои заказы'")
    bot.delete_message(message.chat.id, message.message_id)
    food_order_manager.update_all_orders()
    orders = food_order_manager.get_user_orders(user_id)
    if orders:
        for order in orders:
            bot.send_message(message.chat.id, f"Заказ #{order[0]}: {order[2]}, Сумма: {order[3]} руб.")
    else:
        bot.send_message(message.chat.id, "У вас пока нет заказов.")
    food_order_manager.db_manager.close()

# Специальная команда для админа
@bot.message_handler(commands=['admin'])
def admin_command(message):
    if message.text == '/admin_secret_command':
        bot.send_message(message.chat.id, "Пожалуйста, загрузите CSV файл.")
        bot.register_next_step_handler(message, handle_csv)

# Обработка CSV файла
def handle_csv(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("uploaded_file.csv", "wb") as f:
            f.write(downloaded_file)
        bot.send_message(message.chat.id, "CSV файл успешно загружен.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, загрузите CSV файл.")

@bot.message_handler(func=lambda message: True)
def handle_unprocessed_messages(message):
    print(f"Необработанное сообщение от {message.from_user.username or message.from_user.first_name}: {message.text}")

# Оформление заказа
@bot.callback_query_handler(func=lambda call: call.data==('Оформить заказ'))
def handle_close_order_callback(call):
    user_id = call.from_user.id
    if user_id in user_data and "order_id" in user_data[user_id]:
        del user_data[user_id]["order_id"]
    bot.send_message(call.id, "Сколько вы хотите?")
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Удаление блюда из заказа
@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_'))
def handle_delete_callback(call):
    # Извлекаем данные после 'delete_'
    user_id = call.from_user.id
    if user_id in user_data and "order_form" in user_data[user_id] :
        item_to_delete = call.data[len('delete_'):]
    else:
        bot.send_message(call.message.chat.id, "Сессия была прервана. Используйте нижнее меню")
        trigger_start(call.message)
        return


    # Выполняем удаление
    food_order_manager = init_fo_manager()
    food_order_manager.delete_order_item(item_to_delete)
    food_order_manager.update_all_orders()
    order_items = food_order_manager.get_order_items(user_data[call.from_user.id]["order_id"])
    if len(order_items) == 0:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Ваш заказ пуст.")
        return
    total_price = sum(item[2] * item[3] for item in order_items)  # price * quantity
    title = f"<b>Ваш заказ</b> :  {total_price} руб."
    bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text=title,
                                  reply_markup=create_keyboard_variable_rows(order_items),
                                  parse_mode='HTML')
    bot.send_message(call.message.chat.id, "Пункт заказа удален.")


# Добавление блюда в заказ
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    print(f"Callback query from {call.from_user.username or call.from_user.first_name}: {call.data}")
    user_id = call.from_user.id
    quantity = int(call.data)
    print(user_data)

    if len(user_data) == 0:
        bot.send_message(call.id, "Сессия была прервана. Используйте нижнее меню")
        trigger_start(call.message)

    if user_data[user_id]["step"] != "Item_quantity":
        bot.send_message(call.message.chat.id, "Сессия была прервана. Используйте нижнее меню")
        return

    if user_id not in user_data or 'selected_item' not in user_data[user_id]:
        bot.send_message(call.message.chat.id, "Ошибка: блюдо не выбрано.")
        return

    food_order_manager = init_fo_manager()
    item_name = user_data[user_id]['selected_item']
    item = food_order_manager.get_menu_item_id_by_name(item_name)[0]
    bot.delete_message(call.message.chat.id, call.message.message_id)

    #item = next(item for item in food_order_manager.get_menu_items() if item[2] == item_name)


    # Создание заказа, если его еще нет
    if 'order_id' not in user_data[user_id]:
        order_pending = food_order_manager.get_user_orders_by_status(user_id)[-1]
        if len(order_pending) > 0:
            user_data[user_id]['order_id'] = order_pending[0]
            bot.send_message(call.message.chat.id, "Найден незавершенный заказ. Продолжаю заполнение")
        else:
            order_id = str(uuid.uuid4())
            user_data[user_id]['order_id'] = order_id
            food_order_manager.create_order(user_id, total_price=0)

    # Добавление блюда в заказ
    food_order_manager.add_item_to_order(user_data[user_id]['order_id'], item[0], quantity)
    bot.send_message(call.message.chat.id, f"{quantity} порций '{item_name}' добавлено в заказ!")
    food_order_manager.update_all_orders()



# Запуск бота
bot.polling(none_stop=True)
