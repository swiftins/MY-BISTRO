import telebot
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = "ТВОЙ_ТОКЕН"  # Укажи свой токен от BotFather
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = KeyboardButton(
        text="Оставить отзыв",
        web_app=WebAppInfo(url="https://username.github.io/telegram-webapp-reviews/")  # Твой GitHub Pages
    )
    keyboard.add(webapp_button)
    bot.send_message(message.chat.id, "Оставьте ваш отзыв:", reply_markup=keyboard)

@bot.message_handler(content_types=['web_app_data'])
def webapp_feedback(message):
    try:
        data = json.loads(message.web_app_data.data)
        review = data.get("review", "Ошибка при получении отзыва")
        bot.send_message(message.chat.id, f"Спасибо за ваш отзыв: {review}")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при обработке отзыва.")

bot.polling(none_stop=True)
