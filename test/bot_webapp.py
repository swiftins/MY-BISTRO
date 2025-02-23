import telebot
import json, os
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# Загружаем переменные окружения
env_path = os.path.join(os.path.dirname(__file__), "..", ".venv", ".env")
load_dotenv(env_path)
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = KeyboardButton(
        text="Оставить отзыв",
        web_app=WebAppInfo(url="https://iiipek.github.io/web_app_form/")  # Твой GitHub Pages
    )
    keyboard.add(webapp_button)
    bot.send_message(message.chat.id, "Оставьте ваш отзыв:", reply_markup=keyboard)

@bot.message_handler(content_types=['web_app_data'])
def webapp_feedback(message):
    try:
        data = json.loads(message.web_app_data.data)
        review = data.get("review", "Ошибка при получении отзыва")
        rating = data.get("rating", "Не указан")

        response = f"⭐ Оценка: {rating}/5\n💬 Отзыв: {review}"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при обработке отзыва.")

bot.polling(none_stop=True)
