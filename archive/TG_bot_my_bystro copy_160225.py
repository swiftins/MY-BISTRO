
### Основной файл бота (TG_bot_my_bystro.py)

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
from models import session, Category, Dish  # Импортируем сессию и модели
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

# Запускаем бота
if __name__ == '__main__':
    bot.polling(none_stop=True)