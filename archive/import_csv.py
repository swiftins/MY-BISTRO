import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Dish, Order, OrderItem, Feedback  # Предполагается, что ваши модели уже определены в файле models.py

DATABASE_URL = 'sqlite:///food_order_bot.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Функция для загрузки данных из CSV файла в таблицу
def load_data_from_csv(file_path, model):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Удаляем пробелы у ключей и значений
            cleaned_row = {k.strip(): (v.strip() if v else None) for k, v in row.items()}
            # Преобразуем строку даты в объект datetime
            if 'created_at' in cleaned_row and cleaned_row['created_at']:
                cleaned_row['created_at'] = datetime.strptime(cleaned_row['created_at'], '%Y-%m-%d %H:%M:%S')
            # Преобразуем строки в объекты модели, добавляя проверку на обязательные поля
            try:
                obj = model(**cleaned_row)
                session.add(obj)
            except Exception as e:
                print(f"Ошибка при добавлении объекта: {e}")
    session.commit()

# Загрузка данных
try:
    load_data_from_csv('My_bistro/csv_for_import/orders.csv', Order)
    print("Данные загружены успешно.")
except Exception as e:
    print(f"Ошибка при загрузке данных: {e}")
finally:
    session.close()
