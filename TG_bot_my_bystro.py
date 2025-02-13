import  telebot
from models import *

from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить API-ключ
telegram_api_key = os.getenv('TELEGRAM_API_KEY')

# Используйте API-ключ для инициализации бота
# bot = telegram.Bot(token=telegram_api_key)

# Создайте экземпляр бота
bot = telebot.TeleBot(telegram_api_key)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в систему заказа еды! Используйте /menu для просмотра меню.")

@bot.message_handler(commands=['menu'])
def show_menu(message):
    # Получаем меню из базы данных
    menu_items = session.query(Dish).all()
    menu_message = "Меню:\n"
    for item in menu_items:
        menu_message += f"{item.name} - {item.price}₽\n"
    bot.reply_to(message, menu_message)

# Запускбота
bot.polling()