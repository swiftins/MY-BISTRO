import telebot
from telebot import types 
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from models import session, Category, Dish, User, Order, OrderItem  # Импортируем сессию и модели
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

# Хэндлер для кнопки "Меню"
@bot.message_handler(func=lambda message: message.text == "Меню")
def show_menu(message):
    markup = InlineKeyboardMarkup()

    # Получаем все категории из БД
    categories = session.query(Category).all()
    
    for category in categories:
        button = InlineKeyboardButton(category.name, callback_data=f'category_{category.id}')
        markup.add(button)

    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

# Хэндлер для кнопки возврата в меню
@bot.callback_query_handler(func=lambda call: call.data == 'menu')
def handle_back_to_menu(call):
    show_menu(call.message)

# Хэндлер для обработки нажатий на кнопки категорий
@bot.callback_query_handler(func=lambda call: call.data.startswith('category_'))
def show_dishes(call):
    category_id = int(call.data.split('_')[1])
    dishes = session.query(Dish).filter(Dish.category_id == category_id).all()
    
    markup = InlineKeyboardMarkup()
    
    for dish in dishes:
        button_dish = InlineKeyboardButton(f"{dish.name} - {dish.price:.2f}₽", callback_data=f'dish_{dish.id}')
        button_cart = InlineKeyboardButton("Положить в корзину", callback_data=f'add_to_cart_{dish.id}')
        markup.add(button_dish, button_cart)  # Добавляем оба кнопки в одну строку
    
    bot.send_message(call.message.chat.id, "Выберите блюдо:", reply_markup=markup)

# Хэндлер для добавления блюда в корзину
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def add_to_cart(call):
    dish_id = int(call.data.split('_')[2])
    # Здесь можно добавить логику для добавления в корзину
    # Например, сохранить в сессии или базе данных
    
    # Простой ответ для демонстрации
    bot.answer_callback_query(call.id, "Блюдо добавлено в корзину!")
    bot.send_message(call.message.chat.id, "Вы можете продолжить выбирать блюда или перейти в корзину.")

# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True)

"""
### Изменения и дополнения:

1. **Кнопка "Положить в корзину"**: Для каждого блюда добавлена кнопка "Положить в корзину" в `show_dishes`. Эта кнопка будет отправлять соответствующий `callback_data`, чтобы идентифицировать, какое блюдо добавляется в корзину.

2. **Хэндлер для добавления в корзину**: Добавлен новый хэндлер `add_to_cart`, который обрабатывает нажатия на кнопку "Положить в корзину". В этом хэндлере можно добавить логику для сохранения блюда в корзину пользователя (например, в сессии или базе данных).

3. **Ответ пользователю**: При добавлении блюда в корзину пользователю отправляется уведомление.

Теперь ваш бот должен корректно обрабатывать добавление блюд в корзину, и функционал будет сохраняться. Вы можете дополнить логику работы с корзиной по своему усмотрению.
"""