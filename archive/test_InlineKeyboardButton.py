import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import func
# from models import session, Category, Dish, Order, OrderItem, User
from dotenv import load_dotenv
import os

# Загрузить переменные окружения из файла .env
load_dotenv()

# Получить API-ключ
telegram_api_key = os.getenv('TELEGRAM_API_KEY')

# Создайте экземпляр бота
bot = telebot.TeleBot(telegram_api_key)

@bot.message_handler(commands=['start'])
def start(message):
    # Создание инлайн кнопок
    keyboard = InlineKeyboardMarkup()
    row = [
        InlineKeyboardButton("Кнопка 1", callback_data='button1'),
        InlineKeyboardButton("Кнопка 2", callback_data='button2'),
        InlineKeyboardButton("Кнопка 3", callback_data='button3'),
        InlineKeyboardButton("Кнопка 4", callback_data='button4')
    ]
    keyboard.row(*row)  # Добавление кнопок в одну строку

    # Отправка сообщения с инлайн кнопками
    bot.send_message(message.chat.id, "Выберите кнопку:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # Ответ на нажатие кнопки
    bot.answer_callback_query(call.id)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"Вы нажали: {call.data}"
    )

if __name__ == '__main__':
    bot.polling(none_stop=True)