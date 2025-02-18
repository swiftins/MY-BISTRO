### Основной файл бота (TG_bot_my_bystro.py)

import telebot
from telebot import types 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
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


# Страница Dish
# # Основной файл бота (TG_bot_my_bystro.py)


"""
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func
from models import session, Category, Dish, Order, OrderItem, User
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить API-ключ
telegram_api_key = os.getenv('TELEGRAM_API_KEY')

# Создайте экземпляр бота
bot = telebot.TeleBot(telegram_api_key)

# Хэндлер для кнопки "Меню"
@bot.message_handler(func=lambda message: message.text == "Меню")
def show_menu(message):
    markup = InlineKeyboardMarkup()
    
    # Получаем все категории из БД
    categories = session.query(Category).all()
    
    for category in categories:
        button = InlineKeyboardButton(
        category.name,
        callback_data=f'My_bistro/emoji_category/{category.id}.txt+category_{category.id}'
)
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Хэндлер для выбора категории
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def show_dishes(call):
    category_id = int(call.data.split('_')[1])
    dishes = session.query(Dish).filter(Dish.category_id == category_id).all()

    markup = InlineKeyboardMarkup()
    for dish in dishes:
        button = InlineKeyboardButton(dish.name, callback_data=f'dish_{dish.id}')
        markup.add(button)

    bot.send_message(call.message.chat.id, "Выберите блюдо:", reply_markup=markup)
"""
# Хэндлер для выбора блюда
@bot.callback_query_handler(func=lambda call: call.data.startswith('dish_'))
def show_dish_details(call):
    dish_id = int(call.data.split('_')[1])
    dish = session.query(Dish).filter(Dish.id == dish_id).first()

    # Проверяем, существует ли блюдо
    if not dish:
        bot.send_message(call.message.chat.id, "Блюдо не найдено.")
        return

    # Получаем или создаем пользователя
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    if not user:
        user = User(telegram_id=call.from_user.id, username=call.from_user.username)
        session.add(user)
        session.commit()

    # Резервируем заказ для пользователя, если это первый визит
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()
    if not order:
        order = Order(user_id=user.id, status='active', total_price=0)
        session.add(order)
        session.commit()

    # Отправляем детали блюда
    markup = InlineKeyboardMarkup()

    # Кнопка возврата в меню
    back_button = InlineKeyboardButton("↩️ Назад в меню", callback_data='menu')
    markup.add(back_button)

    # Если есть изображение
   # Проверяем наличие атрибута photo и его значение
    if hasattr(dish, 'photo') and dish.photo:
        bot.send_photo(call.message.chat.id, dish.photo)
    else:
    # Здесь можно добавить обработку случая, когда фото нет
        bot.send_message(call.message.chat.id, "Изображение не найдено.")
    # Отправляем информацию о блюде
    bot.send_message(call.message.chat.id, f"**{dish.name}**\n{dish.description}\n\n**Цена:** {dish.price}", parse_mode='Markdown', reply_markup=markup)

    # Количество и стоимость
    quantity = 1  # Начальное количество
    order_item = session.query(OrderItem).filter(OrderItem.order_id == order.id, OrderItem.dish_id == dish.id).first()
    if order_item:
        quantity = order_item.quantity  # Если уже есть в заказе, берем текущее количество

####################################################

# Функция для создания клавиатуры
def create_keyboard(price, quantity):
    keyboard = types.InlineKeyboardMarkup()
    button_minus = types.InlineKeyboardButton(text='-', callback_data='minus')
    button_plus = types.InlineKeyboardButton(text='+', callback_data='plus')
    button_kol = types.InlineKeyboardButton(text=f'Количество: {quantity}', callback_data='kol')
    button_itogo = types.InlineKeyboardButton(text=f'Итого: {price * quantity}', callback_data='itogo')

    # Расположение кнопок в рядах
    keyboard.add(button_minus, button_plus)
    keyboard.add(button_kol, button_itogo)

    return keyboard

    bot.send_message(message.chat.id, "Управление количеством и итоговой суммой:", reply_markup=create_keyboard(dish.price, quantity))

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global kol

    if call.data == 'plus':
       quantity += 1
    elif call.data == 'minus' and quantity > 1:
       quantity -= 1

    # Обновляем кнопки и отправляем новое сообщение с обновленной информацией
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=create_keyboard(dish.price, quantity))
    
    # Также можно отправить сообщение с обновленной информацией
    bot.answer_callback_query(call.id, text=f'Количество: {kol}\nИтого: {price * kol}', show_alert=True)

####################################################

# Хэндлер для увеличения количества
@bot.callback_query_handler(func=lambda call: call.data.startswith('increase_quantity_'))
def increase_quantity(call):
    dish_id = int(call.data.split('_')[2])
    order_item = session.query(OrderItem).filter(OrderItem.order_id == Order.id, OrderItem.dish_id == dish_id).first()
    
    if order_item:
        order_item.quantity += 1  # Увеличиваем количество на 1
        session.commit()  # Сохраняем изменения в базе данных
        quantity = order_item.quantity
    else:
        quantity = 1  # Если блюда нет в заказе, устанавливаем количество в 1

    # Обновляем вьюху с новыми значениями
    quantity_markup = InlineKeyboardMarkup()
    quantity_markup.add(InlineKeyboardButton("Количество ➕", callback_data=f'increase_quantity_{dish_id}'))
    quantity_markup.add(InlineKeyboardButton(f"Количество: {quantity}", callback_data='dummy'))
    quantity_markup.add(InlineKeyboardButton("Количество ➖", callback_data=f'decrease_quantity_{dish_id}'))
    quantity_markup.add(InlineKeyboardButton(f"Стоимость: {Dish.price * quantity}", callback_data='dummy'))
    quantity_markup.add(InlineKeyboardButton("🛒 Отправить в корзину", callback_data=f'add_to_cart_{dish_id}_{quantity}'))

    bot.edit_message_text("Коррекция количества:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=quantity_markup)

# Хэндлер для уменьшения количества
@bot.callback_query_handler(func=lambda call: call.data.startswith('decrease_quantity_'))
def decrease_quantity(call):
    dish_id = int(call.data.split('_')[2])
    order_item = session.query(OrderItem).filter(OrderItem.order_id == Order.id, OrderItem.dish_id == dish_id).first()
    
    if order_item and order_item.quantity > 1:
        order_item.quantity -= 1  # Уменьшаем количество на 1
        session.commit()  # Сохраняем изменения в базе данных
        quantity = order_item.quantity
    else:
        quantity = 1  # Если количество меньше или равно 1, оставляем его как 1

    # Обновляем вьюху с новыми значениями
    quantity_markup = InlineKeyboardMarkup()
    quantity_markup.add(InlineKeyboardButton("Количество ➕", callback_data=f'increase_quantity_{dish_id}'))
    quantity_markup.add(InlineKeyboardButton(f"Количество: {quantity}", callback_data='dummy'))
    quantity_markup.add(InlineKeyboardButton("Количество ➖", callback_data=f'decrease_quantity_{dish_id}'))
    quantity_markup.add(InlineKeyboardButton(f"Стоимость: {Dish.price * quantity}", callback_data='dummy'))
    quantity_markup.add(InlineKeyboardButton("🛒 Отправить в корзину", callback_data=f'add_to_cart_{dish_id}_{quantity}'))

    bot.edit_message_text("Коррекция количества:", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=quantity_markup)

#######################################################

# Хэндлер для добавления в корзину
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def add_to_cart(call):
    dish_id, quantity = map(int, call.data.split('_')[2:])
    user = session.query(User).filter(User.telegram_id == call.from_user.id).first()
    order = session.query(Order).filter(Order.user_id == user.id, Order.status == 'active').first()
    
    # Добавляем блюдо в корзину
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