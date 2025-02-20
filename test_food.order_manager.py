from db_module import DBConnector, DBManager
from order_manager import FoodOrderManager

# Инициализация подключения к базе данных
db_connector = DBConnector('sqlite')
db_manager = DBManager(db_connector)
food_order_manager = FoodOrderManager(db_manager)

# Создание пользователя
#food_order_manager.create_user(123456, "john_doe", "John", "Doe")
telegram_id = 123456
username = "john_doe"

if food_order_manager.check_user_exists(telegram_id=telegram_id):
    print("Пользователь с таким telegram_id уже существует.")
elif food_order_manager.check_user_exists(username=username):
    print("Пользователь с таким username уже существует.")
else:
    # Создание нового пользователя
    food_order_manager.create_user(telegram_id, username, "John", "Doe")
    print("Новый пользователь создан.")

# Получение категорий меню
categories = food_order_manager.get_menu_categories()
print("Категории меню:", categories)

# Получение блюд из категории
menu_items = food_order_manager.get_menu_items(category_id=None)
print("Блюда из категории All:", menu_items)

# Создание заказа
user_id = "user_id_из_базы_данных"
food_order_manager.create_order(user_id, total_price=100)

# Добавление блюда в заказ
order_id = "order_id_из_базы_данных"
food_order_manager.add_item_to_order(order_id, menu_item_id=1, quantity=2)

# Получение заказов пользователя
orders = food_order_manager.get_user_orders(user_id)
print("Заказы пользователя:", orders)

# Получение блюд в заказе
order_items = food_order_manager.get_order_items(order_id)
print("Блюда в заказе:", order_items)

# Обновление статуса заказа
food_order_manager.update_order_status(order_id, "completed")

# Удаление заказа
food_order_manager.delete_order(order_id)

# Закрытие соединения с базой данных
db_manager.close()
