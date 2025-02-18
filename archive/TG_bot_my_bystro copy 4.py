### Основной файл бота (TG_bot_my_bystro.py)
import telebot
from telebot import types 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func
import random
# Импортируем сессию и модели
from models import session, Category, Dish, User, Order, OrderItem, Session
# Импортируем сессию и модели
from dotenv import load_dotenv
import os
import re  # Импортируем модуль re

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить API-ключ
telegram_api_key = os.getenv('TELEGRAM_API_KEY')

# Создайте экземпляр бота
bot = telebot.TeleBot(telegram_api_key)

# Список изображений для отображения при старте
image_folder = os.path.join(os.getcwd(), 'My_bistro/image')
images = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith('.jpg')]

current_quantities = {}

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

# Хэндлер для нажатия на кнопку блюда на странице меню
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
# Словарь для хранения текущего количества для каждого блюда


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
        types.InlineKeyboardButton("🛒 Отправить в корзину", callback_data=f'add_to_cart_{dish_id}')
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
    
    # Увеличиваем локальное количество
    current_quantities[dish_id] = current_quantities.get(dish_id, 0) + 1
    quantity = current_quantities[dish_id]

    update_quantity_markup(call.message.chat.id, call.message.message_id, dish_id, quantity)

# Хэндлер для уменьшения количества
@bot.callback_query_handler(func=lambda call: call.data.startswith('decrease_quantity_'))
def decrease_quantity(call):
    
    dish_id = int(call.data.split('_')[2])
    
    # Уменьшаем локальное количество
    if dish_id in current_quantities and current_quantities[dish_id] > 0:
        current_quantities[dish_id] = max(0, current_quantities[dish_id] - 1)
    quantity = current_quantities.get(dish_id, 0)

    update_quantity_markup(call.message.chat.id, call.message.message_id, dish_id, quantity)

# Хэндлер для добавления в корзину
# Хэндлер для отправки в корзину
# Хэндлер для отправки в корзину
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def add_to_cart(call):

    dish_id = None  # Инициализация переменной по умолчанию
    parts = call.data.split('_')  # Разбиваем строку на части
    
    # Проверяем, что у нас достаточно частей
    if len(parts) < 3:
        bot.send_message(call.message.chat.id, "Ошибка: недопустимые данные в запросе.")
        return
    
    # Используем регулярное выражение, чтобы проверить, что dish_id является числом
    if not re.match(r'^\d+$', parts[3]):
        bot.send_message(call.message.chat.id, f"Ошибка: идентификатор блюда некорректен: {parts[3]}, {parts[2]},{parts[1]},{parts[0]}")
        return
    
    dish_id = int(parts[3])  # Извлекаем dish_id из callback_data

    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()

    if not order:
        bot.send_message(call.message.chat.id, "У вас нет активного заказа.")
        return

    quantity = current_quantities.get(dish_id, 0)

    if quantity > 0:
        order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish_id).first()

        if order_item:
            order_item.quantity += quantity
        else:
            order_item = OrderItem(order_id=order.id, dish_id=dish_id, quantity=quantity)
            session.add(order_item)

        session.commit()  # Сохраняем изменения в базе данных

        # Очищаем количество после добавления в корзину
        current_quantities[dish_id] = 0

        bot.send_message(call.message.chat.id, f"Вы добавили {quantity} порций блюда в корзину.")
    else:
        bot.send_message(call.message.chat.id, "Количество должно быть больше нуля.")

#############################################################################################################
#############################################################################################################


# Хэндлер для кнопки "Корзинаю"
@bot.message_handler(func=lambda message: message.text == "Корзина")


def show_cart(message):
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return

    orders = session.query(Order).filter_by(user_id=user.id, status='active').first()
    if not orders:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return
    print (orders.id)
    order_items = session.query(OrderItem).filter_by(order_id=orders.id).all()
    total_price = 0

    markup = types.InlineKeyboardMarkup()
    
    for item in order_items:
        dish = session.query(Dish).filter_by(id=item.dish_id).first()
        if dish:
            total_price += dish.price * item.quantity
            
            # Кнопки +, - и Удалить
            row = [
                types.InlineKeyboardButton("+", callback_data=f"increase_{item.id}"),
                types.InlineKeyboardButton("-", callback_data=f"decrease_{item.id}"),
                types.InlineKeyboardButton("Удалить", callback_data=f"remove_{item.id}"),
            ]
            markup.add(*row)

            # Фото блюда
            if hasattr(dish, 'photo') and dish.photo:  # Предполагается, что у вас есть поле image в модели Dish
                bot.send_photo(message.chat.id, dish.image, caption=f"{dish.name}\nЦена: {dish.price}\nКоличество: {item.quantity}")
            else:
                bot.send_message(message.chat.id, "Изображение не найдено.")  # Здесь заменено call на message
                bot.send_message(message.chat.id, f"{dish.name}\nЦена: {dish.price}\nКоличество: {item.quantity}")


    # Кнопки "Стоимость заказа" и "Оформить заказ"
    markup.add(types.InlineKeyboardButton(f"Стоимость заказа: {total_price}", callback_data="total_price"))
    markup.add(types.InlineKeyboardButton("Оформить заказ", callback_data="checkout"))

    bot.send_message(message.chat.id, "Ваши блюда в корзине:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user = session.query(User).filter_by(telegram_id=call.from_user.id).first()
    orders = session.query(Order).filter_by(user_id=user.id, status='active').first()
    
    if call.data.startswith("increase_"):
        item_id = int(call.data.split("_")[1])
        order_item = session.query(OrderItem).filter_by(id=item_id).first()
        if order_item:
            order_item.quantity += 1
            session.commit()
    
    elif call.data.startswith("decrease_"):
        item_id = int(call.data.split("_")[1])
        order_item = session.query(OrderItem).filter_by(id=item_id).first()
        if order_item and order_item.quantity > 1:
            order_item.quantity -= 1
            session.commit()
    
    elif call.data.startswith("remove_"):
        item_id = int(call.data.split("_")[1])
        order_item = session.query(OrderItem).filter_by(id=item_id).first()
        if order_item:
            session.delete(order_item)
            session.commit()
    
    elif call.data == "checkout":
        # Логика для оформления заказа
        bot.send_message(call.message.chat.id, "Заказ оформлен!")

def create_order(user_id, items):
	session = Session()
	try:
		# Создаем новый заказ
		new_order = Order(user_id=user_id)
		session.add(new_order)
		session.flush()  # Сохраняем заказ, чтобы получить его ID

		# Создаем записи для каждого элемента заказа
		for item in items:
			order_item = OrderItem(order_id=new_order.id, item_id=item['item_id'], quantity=item['quantity'])
			session.add(order_item)

		session.commit()  # Сохраняем все изменения
		return new_order.id
	except Exception as e:
		session.rollback()  # Откатываем транзакцию в случае ошибки
		print(f"Error occurred: {e}")
	finally:
		session.close()

@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def handle_checkout(call):
	user_id = call.message.chat.id
	# Предположим, что у вас есть список товаров в корзине
	items_in_cart = [
		{'item_id': 1, 'quantity': 2},  # Пример товара
		{'item_id': 2, 'quantity': 1},
	]

	order_id = create_order(user_id, items_in_cart)
	if order_id:
		bot.send_message(call.message.chat.id, "Заказ оформлен! Номер вашего заказа: {}".format(order_id))
	else:
		bot.send_message(call.message.chat.id, "Произошла ошибка при оформлении заказа.")
	# Обновляем корзину
	show_cart(call.message)


        
# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)