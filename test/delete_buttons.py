import telebot
from telebot import types

API_TOKEN = '7265481895:AAEiGtEWswZa-Jz0CMf63j-zn9-wWcaOzME'

bot = telebot.TeleBot(API_TOKEN)

# Изначальный двумерный массив
data = [
    ["Item 1-1", "Item 1-2", "Item 1-3"],
    ["Item 2-1", "Item 2-2", "Item 2-3"],
    ["Item 3-1", "Item 3-2", "Item 3-3"],
]


# Функция создания инлайн-клавиатуры
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    for index, row in enumerate(data):
        buttons = [types.InlineKeyboardButton(text=col, callback_data="noop") for col in row]
        buttons.append(types.InlineKeyboardButton(text="❌", callback_data=f"delete_{index}"))
        keyboard.add(*buttons)
    return keyboard


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Вот кнопки:", reply_markup=create_keyboard())


# Обработка нажатий на inline-кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("delete_"):
        # Получаем индекс строки для удаления
        index = int(call.data.split("_")[1])
        if 0 <= index < len(data):
            del data[index]  # Удаляем строку из массива

            # Обновляем сообщение с кнопками
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=create_keyboard())


# Запуск бота
bot.infinity_polling()