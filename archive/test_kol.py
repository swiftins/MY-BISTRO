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

# Исходные переменные
price = 150
kol = 1

# Функция для создания клавиатуры
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button_minus = types.InlineKeyboardButton(text='-', callback_data='minus')
    button_plus = types.InlineKeyboardButton(text='+', callback_data='plus')
    button_kol = types.InlineKeyboardButton(text=f'Количество: {kol}', callback_data='kol')
    button_itogo = types.InlineKeyboardButton(text=f'Итого: {price * kol}', callback_data='itogo')

    # Расположение кнопок в рядах
    keyboard.add(button_minus, button_plus)
    keyboard.add(button_kol, button_itogo)

    return keyboard

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Управление количеством и итоговой суммой:", reply_markup=create_keyboard())

# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global kol

    if call.data == 'plus':
        kol += 1
    elif call.data == 'minus' and kol > 1:
        kol -= 1

    # Обновляем кнопки и отправляем новое сообщение с обновленной информацией
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=create_keyboard())
    
    # Также можно отправить сообщение с обновленной информацией
    bot.answer_callback_query(call.id, text=f'Количество: {kol}\nИтого: {price * kol}', show_alert=True)

# Запускаем бота
bot.polling(none_stop=True)

