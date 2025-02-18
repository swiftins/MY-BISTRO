from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import os

# name_path = 'My_bistro'
# Получаем абсолютный путь к каталогу, где находится текущий файл
# current_directory = os.path.dirname(os.path.abspath(name_path))
# DATABASE_URL = f'sqlite:///{os.path.join(current_directory, "food_order_bot.db")}'
# print (current_directory)
# Создаем базу данных и подключаемся к ней
DATABASE_URL = 'sqlite:///food_order_bot.db'
# current_directory = os.path.dirname(os.path.abspath(name_path))
# DATABASE_URL = f'sqlite:///{os.path.join(current_directory, "food_order_bot.db")}'
engine = create_engine(DATABASE_URL)
Base = declarative_base()
# Создание сессии - подключение к БД
Session = sessionmaker(bind=engine)
session = Session()

"""
### Модели для базы данных

1. **Модель `User`**: Для хранения информации о пользователях.
2. **Модель `Restaurant`**: Для хранения информации о ресторанах.
3. **Модель `Dish`**: Для хранения информации о блюдах в меню.
4. **Модель `Order`**: Для хранения информации о заказах.
5. **Модель `OrderItem`**: Для хранения информации о блюдах в заказах.
6. **Модель `Feedback`**: Для хранения отзывов о блюдах и ресторанах.
"""

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String)
    orders = relationship('Order', back_populates='user')

# Модель категорий
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    dishes = relationship('Dish', back_populates='category')

# Модель блюд
class Dish(Base):
    __tablename__ = 'dishes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
# добавить  dish.photo
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='dishes')


# Модель заказа
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')
    status = Column(String)
    total_price = Column(Float)
    created_at = Column(DateTime)
    order_items = relationship('OrderItem', back_populates='order')

# Модель блюда в заказе
class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship('Order', back_populates='order_items')
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    quantity = Column(Integer)
    dish = relationship('Dish')

# Модель отзыва
class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    comment = Column(String)
    rating = Column(Integer)

# Создание всех таблиц в базе данных
try:
    Base.metadata.create_all(engine)
    print("База данных и таблицы созданы успешно.")
except Exception as e:
    print(f"Ошибка: {e}")
