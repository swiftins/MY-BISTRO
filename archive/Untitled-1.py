
Хорошо, давайте доработаем код, чтобы учесть ваши требования. Мы будем использовать фиксированное расположение кнопок, чтобы их положение не менялось при нажатии на кнопки "+" и "-". Также добавим перерасчет общей стоимости и обновление текста кнопки "Стоимость заказа".

Вот обновленный код с учетом всех требований:

```python
import telebot
from telebot import types

# Инициализация бота с вашим токеном
API_TOKEN = 'YOUR_API_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# Заглушка данных о заказах (в реальном приложении это должно быть взаимодействие с БД)
orders = {}

# Функция для получения данных о заказе
def get_order_items(user_id, order_id):
    # Здесь будет логика получения данных из базы данных
    # Для примера создадим фиктивные данные
    items = [
        {'id': 1, 'name': 'Блюдо 1', 'description': 'Описание блюда 1', 'price': 100, 'quantity': 1},
        {'id': 2, 'name': 'Блюдо 2', 'description': 'Описание блюда 2', 'price': 150, 'quantity': 1},
    ]
    return items

# Функция для пересчета общей стоимости
def calculate_total_price(items):
    return sum(item['price'] * item['quantity'] for item in items)

# Показ корзины
def show_cart(message):
    user_id = message.from_user.id
    order_id = orders[user_id]
    items = get_order_items(user_id, order_id)

    total_price = calculate_total_price(items)
    markup = types.InlineKeyboardMarkup()

    for item in items:
        item_text = f"{item['name']} - {item['price']} x {item['quantity']} = {item['price'] * item['quantity']}"
        
        # Кнопки для управления количеством
        plus_button = types.InlineKeyboardButton("+", callback_data=f"plus_{item['id']}")
        minus_button = types.InlineKeyboardButton("-", callback_data=f"minus_{item['id']}")
        delete_button = types.InlineKeyboardButton("Удалить", callback_data=f"delete_{item['id']}")

        # Добавляем кнопки в один ряд
        button_row = types.InlineKeyboardMarkup(row_width=3)
        button_row.add(plus_button, minus_button, delete_button)
        
        # Добавляем текст блюда и кнопки в разметку
        markup.add(types.InlineKeyboardButton(item_text, callback_data="none"), button_row)

    # Кнопка для оформления заказа
    markup.add(types.InlineKeyboardButton(f"Стоимость заказа: {total_price}", callback_data="checkout"))

bot.send_message(message.chat.id, "Ваши блюда в корзине:", reply_markup=markup)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    order_id = 1  # Предположим, что у нас один активный заказ
    orders[user_id] = order_id
    show_cart(message)

# Обработка нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    order_id = orders[user_id]
    
    # Логика обработки кнопок
    items = get_order_items(user_id, order_id)
    
    if call.data.startswith("plus_"):
        item_id = int(call.data.split("_")[1])
        for item in items:
            if item['id'] == item_id:
                item['quantity'] += 1
                break
    elif call.data.startswith("minus_"):
        item_id = int(call.data.split("_")[1])
        for item in items:
            if item['id'] == item_id and item['quantity'] > 1:
                item['quantity'] -= 1
                break
    elif call.data.startswith("delete_"):
        item_id = int(call.data.split("_")[1])
        items = [item for item in items if item['id'] != item_id]

    # Пересчет общей стоимости
    total_price = calculate_total_price(items)
    
    # Обновляем корзину после изменений
    show_cart(call.message)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)


