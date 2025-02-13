# FoodOrderManager

Класс `FoodOrderManager` предназначен для работы с базой данных в контексте заказа еды. Он предоставляет методы для управления меню, пользователями, заказами и их содержимым.

## Установка и настройка

1. Убедитесь, что у вас установлены все необходимые зависимости:
   - `sqlite3` (или другая СУБД, если вы используете PostgreSQL или MySQL).
   - Убедитесь, что база данных инициализирована и таблицы созданы (см. `tables.py`).

2. Импортируйте класс `FoodOrderManager` в ваш проект:
   ```python
   from food_order_manager import FoodOrderManager
   from db_connector import DBConnector
   from db_manager import DBManager
   ```

3. Создайте экземпляр `FoodOrderManager`:
   ```python
   db_connector = DBConnector('sqlite')  # или 'postgresql', 'mysql'
   db_manager = DBManager(db_connector)
   food_order_manager = FoodOrderManager(db_manager)
   ```

## Методы

### 1. **Получение меню**
- **`get_menu_categories()`**  
  Возвращает список всех категорий меню.  
  **Пример:**
  ```python
  categories = food_order_manager.get_menu_categories()
  print(categories)
  ```

- **`get_menu_items(category_id=None)`**  
  Возвращает список блюд. Если указан `category_id`, возвращает блюда только из этой категории.  
  **Пример:**
  ```python
  # Все блюда
  all_items = food_order_manager.get_menu_items()
  print(all_items)

  # Блюда из категории с ID = 1
  category_items = food_order_manager.get_menu_items(category_id=1)
  print(category_items)
  ```

### 2. **Работа с пользователями**
- **`create_user(telegram_id, username, first_name, last_name)`**  
  Создает нового пользователя.  
  **Пример:**
  ```python
  food_order_manager.create_user(123456, "john_doe", "John", "Doe")
  ```

### 3. **Работа с заказами**
- **`create_order(user_id, status="pending", total_price=0)`**  
  Создает новый заказ для пользователя.  
  **Пример:**
  ```python
  order_id = food_order_manager.create_order(user_id="user_id_из_базы", total_price=100)
  print(f"Создан заказ с ID: {order_id}")
  ```

- **`add_item_to_order(order_id, menu_item_id, quantity)`**  
  Добавляет блюдо в заказ.  
  **Пример:**
  ```python
  food_order_manager.add_item_to_order(order_id="order_id_из_базы", menu_item_id=1, quantity=2)
  ```

- **`get_user_orders(user_id)`**  
  Возвращает все заказы пользователя.  
  **Пример:**
  ```python
  orders = food_order_manager.get_user_orders(user_id="user_id_из_базы")
  print(orders)
  ```

- **`get_order_items(order_id)`**  
  Возвращает все блюда в заказе.  
  **Пример:**
  ```python
  order_items = food_order_manager.get_order_items(order_id="order_id_из_базы")
  print(order_items)
  ```

- **`update_order_status(order_id, status)`**  
  Обновляет статус заказа.  
  **Пример:**
  ```python
  food_order_manager.update_order_status(order_id="order_id_из_базы", status="completed")
  ```

- **`delete_order(order_id)`**  
  Удаляет заказ.  
  **Пример:**
  ```python
  food_order_manager.delete_order(order_id="order_id_из_базы")
  ```

## Пример использования

```python
# Инициализация
db_connector = DBConnector('sqlite')
db_manager = DBManager(db_connector)
food_order_manager = FoodOrderManager(db_manager)

# Создание пользователя
food_order_manager.create_user(123456, "john_doe", "John", "Doe")

# Получение меню
categories = food_order_manager.get_menu_categories()
print("Категории меню:", categories)

menu_items = food_order_manager.get_menu_items(category_id=1)
print("Блюда из категории 1:", menu_items)

# Создание заказа
order_id = food_order_manager.create_order(user_id="user_id_из_базы", total_price=100)

# Добавление блюда в заказ
food_order_manager.add_item_to_order(order_id=order_id, menu_item_id=1, quantity=2)

# Получение заказов пользователя
orders = food_order_manager.get_user_orders(user_id="user_id_из_базы")
print("Заказы пользователя:", orders)

# Закрытие соединения
db_manager.close()
```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

