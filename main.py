import telebot
import sqlite3

# Инициализация бота
TOKEN = "7918967502:AAGbpGfUYbw0M5QphKGF0TR-8jnDYJsjEmw"
bot = telebot.TeleBot(TOKEN)

# Подключение к базе данных
def init_db():
    conn = sqlite3.connect("food_orders.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        items TEXT,
        total_price REAL,
        status TEXT DEFAULT 'В обработке'
    )""")
    conn.commit()
    conn.close()

init_db()

# Отображение меню
@bot.message_handler(commands=['menu'])
def show_menu(message):
    conn = sqlite3.connect("food_orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price FROM menu")
    menu_items = cursor.fetchall()
    conn.close()
    
    if not menu_items:
        bot.send_message(message.chat.id, "Меню пока пусто.")
        return
    
    response = "Меню:\n"
    for item in menu_items:
        response += f"{item[0]}. {item[1]} ({item[2]}) - {item[3]} руб.\n"
    bot.send_message(message.chat.id, response)

# Оформление заказа
cart = {}

@bot.message_handler(commands=['add'])
def add_to_cart(message):
    try:
        item_id, quantity = map(int, message.text.split()[1:])
        conn = sqlite3.connect("food_orders.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM menu WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        
        if not item:
            bot.send_message(message.chat.id, "Такого блюда нет в меню.")
            return
        
        if message.chat.id not in cart:
            cart[message.chat.id] = []
        
        cart[message.chat.id].append((item[0], quantity, item[1] * quantity))
        bot.send_message(message.chat.id, f"Добавлено в корзину: {item[0]} x{quantity}")
    except:
        bot.send_message(message.chat.id, "Используйте формат: /add <id блюда> <количество>")

@bot.message_handler(commands=['cart'])
def show_cart(message):
    if message.chat.id not in cart or not cart[message.chat.id]:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return
    
    response = "Ваша корзина:\n"
    total = 0
    for item in cart[message.chat.id]:
        response += f"{item[0]} x{item[1]} - {item[2]} руб.\n"
        total += item[2]
    response += f"Итого: {total} руб."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['order'])
def place_order(message):
    if message.chat.id not in cart or not cart[message.chat.id]:
        bot.send_message(message.chat.id, "Ваша корзина пуста.")
        return
    
    items_list = ", ".join([f"{item[0]} x{item[1]}" for item in cart[message.chat.id]])
    total_price = sum(item[2] for item in cart[message.chat.id])
    
    conn = sqlite3.connect("food_orders.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, items, total_price) VALUES (?, ?, ?)", 
                   (message.chat.id, items_list, total_price))
    conn.commit()
    conn.close()
    
    cart[message.chat.id] = []
    bot.send_message(message.chat.id, f"Ваш заказ оформлен! Итоговая сумма: {total_price} руб.")

@bot.message_handler(commands=['status'])
def order_status(message):
    conn = sqlite3.connect("food_orders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, items, status FROM orders WHERE user_id = ?", (message.chat.id,))
    orders = cursor.fetchall()
    conn.close()
    
    if not orders:
        bot.send_message(message.chat.id, "У вас нет активных заказов.")
        return
    
    response = "Ваши заказы:\n"
    for order in orders:
        response += f"Заказ {order[0]}: {order[1]} - Статус: {order[2]}\n"
    bot.send_message(message.chat.id, response)

bot.polling(none_stop=True)
