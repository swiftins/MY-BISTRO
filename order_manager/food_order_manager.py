from uuid import uuid4
from db_module import *

class FoodOrderManager:
    def __init__(self, param_db_manager: DBManager= None):
        self.db_manager = param_db_manager

    def check_user_exists(self, telegram_id=None, username=None):
        """
        Проверяет, существует ли пользователь с указанным telegram_id или username.
        Возвращает True, если пользователь существует, иначе False.
        """
        if telegram_id:
            query = "SELECT id FROM users WHERE telegram_id = ?"
            params = (telegram_id,)
        elif username:
            query = "SELECT id FROM users WHERE username = ?"
            params = (username,)
        else:
            raise ValueError("Необходимо указать telegram_id или username")

        result = self.db_manager.fetch_data(query, params)
        return bool(result)  # True, если пользователь найден, иначе False

    def get_user_by_telegram_id(self, telegram_id):
        """Получить пользователя по telegram_id."""
        query = "SELECT * FROM users WHERE telegram_id = ?"
        return self.db_manager.fetch_data(query, (telegram_id,))


    def get_menu_categories(self):
        """Получить все категории меню."""
        query = "SELECT * FROM menu_categories"
        return self.db_manager.fetch_data(query)

    def get_menu_items(self, category_id=None):
        """Получить все блюда меню или блюда из конкретной категории."""
        if category_id:
            query = "SELECT * FROM menu_items WHERE category_id = ?"
            return self.db_manager.fetch_data(query, (category_id,))
        else:
            query = "SELECT * FROM menu_items"
            return self.db_manager.fetch_data(query)

    def create_user(self, telegram_id, username, first_name, last_name):
        """Создать нового пользователя."""
        user_id = str(uuid4())
        query = """
            INSERT INTO users (id, telegram_id, username, first_name, last_name)
            VALUES (?, ?, ?, ?, ?)
        """
        params = (user_id, telegram_id, username, first_name, last_name)
        return self.db_manager.insert_data(query, params)

    def create_order(self, user_id, status="pending", total_price=0):
        """Создать новый заказ."""
        order_id = str(uuid4())
        query = """
            INSERT INTO orders (id, user_id, status, total_price)
            VALUES (?, ?, ?, ?)
        """
        params = (order_id, user_id, status, total_price)
        return self.db_manager.insert_data(query, params)

    def add_item_to_order(self, order_id, menu_item_id, quantity):
        """Добавить блюдо в заказ."""
        query = """
            INSERT INTO order_items (order_id, menu_item_id, quantity)
            VALUES (?, ?, ?)
        """
        params = (order_id, menu_item_id, quantity)
        return self.db_manager.insert_data(query, params)

    def get_user_orders(self, user_id):
        """Получить все заказы пользователя."""
        query = "SELECT * FROM orders WHERE user_id = ?"
        return self.db_manager.fetch_data(query, (user_id,))

    def get_order_items(self, order_id):
        """Получить все блюда в заказе."""
        query = """
            SELECT mi.name, mi.price, oi.quantity
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = ?
        """
        return self.db_manager.fetch_data(query, (order_id,))

    def update_order_status(self, order_id, status):
        """Обновить статус заказа."""
        query = "UPDATE orders SET status = ? WHERE id = ?"
        params = (status, order_id)
        return self.db_manager.update_data(query, params)

    def delete_order(self, order_id):
        """Удалить заказ."""
        query = "DELETE FROM orders WHERE id = ?"
        return self.db_manager.delete_data(query, (order_id,))
