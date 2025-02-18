from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy.orm import sessionmaker
from your_database_setup import Dish, engine  # Импортируйте ваши модели и настройки базы данных

bot = TeleBot('YOUR_API_TOKEN')

Session = sessionmaker(bind=engine)
session = Session()

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = InlineKeyboardMarkup()
    # Здесь добавьте кнопки категорий, например:
    # markup.add(InlineKeyboardButton("Категория 1", callback_data='category_1'))
    # markup.add(InlineKeyboardButton("Категория 2", callback_data='category_2'))
    
    bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

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