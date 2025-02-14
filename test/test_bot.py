
import telebot
from telebot import types

TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Нажми меня", callback_data="button_clicked")
    keyboard.add(button)
    bot.send_message(message.chat.id, "Привет! Это inline-кнопка:", reply_markup=keyboard)

# Обработка нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "button_clicked":
        bot.answer_callback_query(call.id, "Кнопка нажата!")  # Всплывающее уведомление
        bot.send_message(call.message.chat.id, "Кнопка нажата!")

# Запуск бота
bot.infinity_polling()
