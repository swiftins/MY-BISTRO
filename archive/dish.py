### bot.py


import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from sqlalchemy.orm import sessionmaker
from models.py import Dish, Order, OrderItem, Session

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_API_TOKEN')
session = Session()

# Переменная для хранения текущих заказов
current_orders = {}

@bot.message_handler(commands=['menu'])
def menu(message):
    # Отправка меню с невидимыми кнопками
    markup = InlineKeyboardMarkup()
    for i in range(40):
        markup.add(InlineKeyboardButton(text="", callback_data=f"button_{i}"))
    bot.send_message(message.chat.id, "Меню", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_dish_selection(call):
    # Получаем id блюда из callback_data
    dish_id = int(call.data.split('_')[1])  # Здесь вы должны получить id блюда
    dish = session.query(Dish).filter(Dish.id == dish_id).first()

    if not current_orders.get(call.from_user.id):
        order = Order()
        session.add(order)
        session.commit()
        current_orders[call.from_user.id] = order.id

    order_id = current_orders[call.from_user.id]

    # Вывод информации о блюде
    category_button = InlineKeyboardButton(text=f"↩️ {dish.category.name}", callback_data=f"back_to_menu")
    markup = InlineKeyboardMarkup()
    markup.add(category_button)

    if dish.photo:
        bot.send_photo(call.message.chat.id, dish.photo)

    bot.send_message(call.message.chat.id, f"{dish.name}\n{dish.description}\n\n"
                                            f"*Цена: {dish.price}*", parse_mode='Markdown', reply_markup=markup)

    # Количество и стоимость
    quantity = 1  # Начальное количество
    total_price = dish.price * quantity

    quantity_markup = InlineKeyboardMarkup()
    quantity_markup.add(
        InlineKeyboardButton("Количество ➕", callback_data=f"increase_{dish.id}"),
        InlineKeyboardButton(f"Количество: {quantity}", callback_data=f"quantity_{dish.id}_{quantity}"),
        InlineKeyboardButton("Количество ➖", callback_data=f"decrease_{dish.id}"),
        InlineKeyboardButton(f"Стоимость: {total_price}", callback_data=f"total_{dish.id}_{total_price}"),
    )
    quantity_markup.add(InlineKeyboardButton("🛒 Отправить в корзину", callback_data=f"add_to_cart_{dish.id}_{quantity}"))

    bot.send_message(call.message.chat.id, "Коррекция количества", reply_markup=quantity_markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('increase_'))
def increase_quantity(call):
    dish_id = int(call.data.split('_')[1])
    # Логика увеличения количества блюда и пересчета общей стоимости

@bot.callback_query_handler(func=lambda call: call.data.startswith('decrease_'))
def decrease_quantity(call):
    dish_id = int(call.data.split('_')[1])
    # Логика уменьшения количества блюда и пересчета общей стоимости

@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart_'))
def add_to_cart(call):
    dish_id, quantity = map(int, call.data.split('_')[2:])
    order_id = current_orders[call.from_user.id]
    order_item = OrderItem(order_id=order_id, dish_id=dish_id, quantity=quantity)
    session.add(order_item)
    session.commit()

    # Пересчет стоимости заказа
    total_order_price = sum(item.dish.price * item.quantity for item in session.query(OrderItem).filter(OrderItem.order_id == order_id))
    bot.send_message(call.message.chat.id, f"Общая стоимость вашего заказа: {total_order_price}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('back_to_menu'))
def back_to_menu(call):
    menu(call.message)

# Запуск бота
bot.polling()
