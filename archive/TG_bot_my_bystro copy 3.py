### Основной файл бота (TG_bot_my_bystro.py)

import telebot
from telebot import types 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func
import random
from models import session, Category, Dish, User, Order, OrderItem # Импортируем сессию и модели
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить API-ключ
telegram_api_key = os.getenv('TELEGRAM_API_KEY')

# Создайте экземпляр бота
bot = telebot.TeleBot(telegram_api_key)

# Список изображений для отображения при старте
image_folder = os.path.join(os.getcwd(), 'My_bistro/image')
images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_photo(message.chat.id, open(random.choice(images), 'rb'))  # Отправка случайного изображения

    # Создаем кнопки
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_menu = telebot.types.KeyboardButton("Меню")
    button_cart = telebot.types.KeyboardButton("Корзина")
    button_profile = telebot.types.KeyboardButton("Профиль")
    
    markup.add(button_menu, button_cart, button_profile)
    
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите опцию:", reply_markup=markup)

# Страница Menu
# Хэндлер для кнопки "Меню"
@bot.message_handler(func=lambda message: message.text == "Меню")
def show_menu(message):
    markup = types.InlineKeyboardMarkup()  # Используйте правильный импорт для InlineKeyboardMarkup

    # Получаем все категории из БД
    categories = session.query(Category).all()
    
    for category in categories:
        button = InlineKeyboardButton(category.name, callback_data=f'category_{category.id}')
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Хэндлер для кнопки возврата в меню
@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_back_to_menu(call):
    # Здесь мы вызываем show_menu и передаем call.message
    show_menu(call.message)
    
 
# Хэндлер для обработки нажатий на кнопки категорий
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def show_dishes(call):
    category_id = int(call.data.split('_')[1])
    dishes = session.query(Dish).filter(Dish.category_id == category_id).all()
    
    markup = InlineKeyboardMarkup()
    
    for dish in dishes:
        button = InlineKeyboardButton(f"{dish.name} - {dish.price:.2f}₽", callback_data=f'dish_{dish.id}')
        markup.add(button)
    
    bot.send_message(call.message.chat.id, "Выберите блюдо:", reply_markup=markup)


# Страница Dish в рамках страницы Menu
# # Основной файл бота (TG_bot_my_bystro.py)
# Хэндлер для выбора блюда

from sqlalchemy import func
from telebot import types

# Хэндлер для нажатия на кнопку блюда
@bot.callback_query_handler(func=lambda call: call.data.startswith('dish_'))
def handle_dish_call(call):
    dish_id = int(call.data.split('_')[1])
    dish = session.query(Dish).filter(Dish.id == dish_id).first()

    if dish:
        send_dish_info(call, dish)

def send_dish_info(call, dish):
    # Получаем текущее количество блюда в заказе
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()

    quantity = 1  # Начальное количество
    if order:
        order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish.id).first()
        if order_item:
            quantity = order_item.quantity

    # Отправка сообщения с информацией о блюде
    bot.send_message(call.message.chat.id, f"{dish.name}\n{dish.description}\n\n**Цена: {dish.price}**", parse_mode='Markdown')

    # Обновляем разметку для выбора количества
    update_quantity_markup(call.message.chat.id, call.message.message_id, dish.id, quantity)

def keyboard(dish_id, quantity, dish_price):
    quantity_markup = types.InlineKeyboardMarkup()

    # Первый ряд
    row1 = [
        types.InlineKeyboardButton("Количество ➕", callback_data=f'increase_quantity_{dish_id}'),
        types.InlineKeyboardButton("Количество ➖", callback_data=f'decrease_quantity_{dish_id}')
    ]
    quantity_markup.row(*row1)  # Добавляем первый ряд кнопок

    # Второй ряд
    row2 = [
        types.InlineKeyboardButton(f"Стоимость: {dish_price * quantity}", callback_data='dummy'),
        types.InlineKeyboardButton(f"Количество: {quantity}", callback_data='dummy'),
        types.InlineKeyboardButton("🛒 Отправить в корзину", callback_data=f'add_to_cart_{dish_id}_{quantity}')
    ]
    quantity_markup.row(*row2)  # Добавляем второй ряд кнопок

    return quantity_markup

def update_quantity_markup(chat_id, message_id, dish_id, quantity):
    # Получаем цену блюда
    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    quantity_markup = keyboard(dish_id, quantity, dish.price)

    bot.edit_message_text("Коррекция количества:", chat_id=chat_id, message_id=message_id, reply_markup=quantity_markup)

# Хэндлер для увеличения количества
@bot.callback_query_handler(func=lambda call: call.data.startswith('increase_quantity_'))
def increase_quantity(call):
    dish_id = int(call.data.split('_')[2])
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()
    
    if not order:
        bot.send_message(call.message.chat.id, "У вас нет активного заказа.")
        return

    order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish_id).first()
    
    if order_item:
        order_item.quantity += 1
    else:
        order_item = OrderItem(order_id=order.id, dish_id=dish_id, quantity=1)
        session.add(order_item)

    session.commit()  # Сохраняем изменения в базе данных
    quantity = order_item.quantity

    update_quantity_markup(call.message.chat.id, call.message.message_id, dish_id, quantity)

# Хэндлер для уменьшения количества
@bot.callback_query_handler(func=lambda call: call.data.startswith('decrease_quantity_'))
def decrease_quantity(call):
    dish_id = int(call.data.split('_')[2])
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()
    
    if not order:
        bot.send_message(call.message.chat.id, "У вас нет активного заказа.")
        return

    order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish_id).first()
    
    if order_item and order_item.quantity > 1:
        order_item.quantity -= 1
        session.commit()  # Сохраняем изменения в базе данных
        quantity = order_item.quantity
    else:
        return  # Не уменьшаем, если уже 1

    update_quantity_markup(call.message.chat.id, call.message.message_id, dish_id, quantity)

# Хэндлер для добавления в корзину
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def add_to_cart(call):
    dish_id, quantity = map(int, call.data.split('_')[2:])
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()

    if not order:
        bot.send_message(call.message.chat.id, "У вас нет активного заказа.")
        return

    order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish_id).first()
    if order_item:
        order_item.quantity += quantity
    else:
        order_item = OrderItem(order_id=order.id, dish_id=dish_id, quantity=quantity)
        session.add(order_item)

    # Обновляем общую стоимость заказа
    total_price = session.query(func.sum(OrderItem.quantity * Dish.price)).join(Dish).filter(OrderItem.order_id == order.id).scalar() or 0
    order.total_price = total_price
    session.commit()

    bot.send_message(call.message.chat.id, "Блюдо добавлено в корзину.")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)