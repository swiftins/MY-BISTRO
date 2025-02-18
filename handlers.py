# handlers.py
from telebot import TeleBot

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

# bot = TeleBot('YOUR_API_TOKEN')  # Замените 'YOUR_API_TOKEN' на токен вашего бота

# Хэндлер для кнопки "Корзина"
@bot.message_handler(func=lambda message: message.text == "Корзина")
def show_cart(message):
    bot.send_message(message.chat.id, "Вы открыли корзину.")

# Хэндлер для кнопки "Профиль"
@bot.message_handler(func=lambda message: message.text == "Профиль")
def show_profile(message):
    bot.send_message(message.chat.id, "Вы открыли профиль.")
