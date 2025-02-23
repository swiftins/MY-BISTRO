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


    def get_menu_categories(self, category_id=None):
        """Получить все категории меню."""
        if category_id:
            query = "SELECT * FROM menu_categories WHERE id = ?"
            return self.db_manager.fetch_data(query, (category_id,))
        else:
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

    def get_menu_item_id_by_name(self, item_name=None):
        """Получить блюдо меню по имени или все блюда."""
        if item_name:
            query = "SELECT * FROM menu_items WHERE name = ?"
            return self.db_manager.fetch_data(query, (item_name,))
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
        return self.db_manager.insert_data(query, params),order_id

    def get_order_status(self, order_id):
        query = "SELECT status FROM orders WHERE id = ?"
        return self.db_manager.fetch_data(query, (order_id,)),order_id

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

    def get_user_orders_by_status(self, user_id, status="pending"):
        """Получить все заказы пользователя."""
        if status:
            query = "SELECT * FROM orders WHERE user_id = ? AND status = ?"
            return self.db_manager.fetch_data(query, (user_id,status))
        else:
            query = "SELECT * FROM orders WHERE user_id = ?"
            return self.db_manager.fetch_data(query, (user_id,))

    def get_order_items(self, order_id):
        """Получить все блюда в заказе."""
        query = """
            SELECT oi.id,mi.name, mi.price, oi.quantity
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = ?
        """
        return self.db_manager.fetch_data(query, (order_id,))

    def update_order_status(self, order_id, status):
        """Обновить статус заказа."""
        text = ""
        if status == "paid":
            text = f", {status}_at = CURRENT_TIMESTAMP"
        query = (f"""UPDATE orders
                 SET status = ? {text}
                 WHERE id = ?"""
                 )
        params = (status, order_id)
        return self.db_manager.update_data(query, params)

    def delete_order(self, order_id):
        """Удалить заказ."""
        query = "DELETE FROM orders WHERE id = ? AND status = 'pending'"
        return self.db_manager.delete_data(query, (order_id,))

    def delete_order_item(self, order_id):
        """Удалить из заказа."""
        query = "DELETE FROM order_items WHERE id = ?"
        return self.db_manager.delete_data(query, (order_id,))


    def update_all_orders(self):
        query="""
            UPDATE orders
            SET total_price = COALESCE(
            (SELECT SUM(oi.quantity * mi.price)
            FROM order_items AS oi
            INNER JOIN menu_items AS mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = orders.id
            GROUP BY oi.order_id
            ), 0);"""
        return self.db_manager.update_data(query)

    def get_order_by_id_or_user_id(self,order_id=None,user_id=None):
        query = """
        SELECT
        o.id,
        (SUBSTR(u.first_name, 1, 1) || SUBSTR(u.last_name, 1, 1) || strftime('%Y%m%d%H%M', datetime(o.created_at))) as order_num,
        SUM(oi.quantity * mi.price) as total,
        (u.first_name||' '||u.last_name) as full_name,
        datetime(o.created_at,'localtime') as created_at,
        coalesce(datetime(o.paid_at,'localtime'),"") as paid_at,
        o.status
        FROM orders as o
        INNER JOIN users as u on u.telegram_id = o.user_id
        LEFT JOIN order_items as oi on o.id = oi.order_id
        LEFT JOIN menu_items as mi on oi.menu_item_id = mi.id
        """
        params = []
        if order_id or user_id:
            query += "WHERE "
        if order_id:
            query += f"o.id = ? "
            params.append(order_id)
            if user_id:
                query += ' and '
        if user_id:
            query += f"o.user_id = ?"
            params.append(user_id)
        query += " GROUP BY o.id;"

        return self.db_manager.fetch_data(query, tuple(params))

    def create_review(self, user_id, review="blank", rating=0):
        """Создать новый отзыв."""
        query = """
            INSERT INTO reviews (user_id, comment, rating)
            VALUES ((SELECT id FROM users WHERE telegram_id = ?), ?, ?)
        """
        params = (user_id, review, rating)
        return self.db_manager.insert_data(query, params)

    def get_reviews(self):
        """Получить все отзывы."""
        query = ("""
                SELECT
                datetime(r.created_at,'localtime') as created_at,
                coalesce(u.first_name,'')||' '|| coalesce(u.last_name,''),
                r.comment,
                r.rating
                FROM reviews as r
                inner join users u on u.id = r.user_id
                """)
        return self.db_manager.fetch_data(query)

def init_fo_manager(db_type='sqlite'):
    db_connector = DBConnector(db_type)
    db_manager = DBManager(db_connector)
    return FoodOrderManager(db_manager)