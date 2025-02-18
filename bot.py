import telebot
from telebot import types
from telebot.types import Message

BOT_TOKEN = "7918967502:AAGbpGfUYbw0M5QphKGF0TR-8jnDYJsjEmw"
#APP_URL = "https://lulu.lv"
APP_URL = "https://43316d88-e1a1-4bfc-a6b1-09df32160a4c-00-10pot8q2x17w2.janeway.replit.dev/"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start_command(message: Message):
    web_app_info = types.WebAppInfo(APP_URL)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_button = types.KeyboardButton("Меню", web_app=web_app_info)
    markup.add(menu_button)
    bot.send_message(message.chat.id, "Нажми на кнопку, чтобы увидеть меню", reply_markup=markup)

bot.polling()
