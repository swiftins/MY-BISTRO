import telebot
from telebot import types
from order_manager import FoodOrderManager
from db_module import DBConnector, DBManager
import uuid
import csv

# Инициализация бота
bot = telebot.TeleBot("7918967502:AAGbpGfUYbw0M5QphKGF0TR-8jnDYJsjEmw")

# Глобальная переменная для максимального количества порций
number_of_seats = 5  # Максимальное количество порций

# Инициализация менеджера заказов
def init_fomanager(db_type='sqlite'):
    db_connector = DBConnector(db_type)
    db_manager = DBManager(db_connector)
    return FoodOrderManager(db_manager)

# Состояния для обработки заказов
user_data = {}

# Команда старта
@bot.message_handler(commands=['start'])
def start(message):
    food_order_manager = init_fomanager()
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Проверка, существует ли пользователь
    if not food_order_manager.check_user_exists(telegram_id=user_id):
        food_order_manager.create_user(user_id, username, first_name, last_name)
        bot.send_message(message.chat.id, "Вы успешно зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "С возвращением!")

    # Отправка главного меню
    show_main_menu(message.chat.id)
    food_order_manager.db_manager.close()

# Показать главное меню
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_menu = types.KeyboardButton('Меню')
    btn_orders = types.KeyboardButton('Мои заказы')
    markup.add(btn_menu, btn_orders)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

# Показать меню
@bot.message_handler(func=lambda message: message.text == 'Меню')
def show_menu(message):
    food_order_manager = init_fomanager()
    categories = food_order_manager.get_menu_categories()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for category in categories:
        markup.add(types.KeyboardButton(category[1]))
    markup.add(types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)
    food_order_manager.db_manager.close()

# Показать блюда в категории
@bot.message_handler(func=lambda message: message.text in [category[1] for category in init_fomanager().get_menu_categories()])
def show_category_items(message):
    food_order_manager = init_fomanager()
    category_name = message.text
    category_id = next(category[0] for category in food_order_manager.get_menu_categories() if category[1] == category_name)
    items = food_order_manager.get_menu_items(category_id=category_id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for item in items:
        markup.add(types.KeyboardButton(f"{item[2]} - {item[4]} руб."))
    markup.add(types.KeyboardButton('Назад'))
    bot.send_message(message.chat.id, "Выберите блюдо:", reply_markup=markup)
    food_order_manager.db_manager.close()

# Обработчик выбора блюда
@bot.message_handler(func=lambda message: message.text.endswith('руб.'))
def select_item_quantity(message):
    user_id = message.from_user.id
    item_name = message.text.split(' - ')[0]

    # Сохраняем выбранное блюдо в user_data
    user_data[user_id] = {'selected_item': item_name}

    # Создаем кнопки для выбора количества
    markup = types.ReplyKeyboardMarkup(row_width=5)
    for i in range(1, number_of_seats + 1):
        markup.add(types.KeyboardButton(str(i)))

    bot.send_message(message.chat.id, f"Сколько порций '{item_name}' вы хотите заказать?", reply_markup=markup)

# Обработчик ввода количества
@bot.message_handler(func=lambda message: message.text.isdigit() and 1 <= int(message.text) <= number_of_seats)
def add_item_to_order(message):
    user_id = message.from_user.id
    quantity = int(message.text)

    if user_id not in user_data or 'selected_item' not in user_data[user_id]:
        bot.send_message(message.chat.id, "Ошибка: блюдо не выбрано.")
        return

    food_order_manager = init_fomanager()
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
    food_order_manager = init_fomanager()
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
    user_id = message.from_user.id

    if 'order_id' not in user_data.get(user_id, {}):
        bot.send_message(message.chat.id, "Ваш заказ пуст.")
        return

    food_order_manager = init_fomanager()
    order_id = user_data[user_id]['order_id']

    # Получаем информацию о заказе
    order_items = food_order_manager.get_order_items(order_id)
    total_price = sum(item[1] * item[2] for item in order_items)  # price * quantity

    # Формируем сообщение с заказом
    order_message = "Ваш заказ:\n"
    for item in order_items:
        order_message += f"{item[0]} - {item[2]} шт. - {item[1] * item[2]} руб.\n"
    order_message += f"Итого: {total_price} руб."

    bot.send_message(message.chat.id, order_message)

    # Очищаем заказ
    del user_data[user_id]['order_id']

    # Возвращаем пользователя в главное меню
    show_main_menu(message.chat.id)
    food_order_manager.db_manager.close()

# Показать заказы пользователя
@bot.message_handler(func=lambda message: message.text == 'Мои заказы')
def show_user_orders(message):
    food_order_manager = init_fomanager()
    user_id = message.from_user.id
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

# Запуск бота
bot.polling(none_stop=True)
