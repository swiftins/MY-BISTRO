class DBSchema:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.connection = db_connector.get_connection()
        self.cursor = self.connection.cursor()

    def create_database(self, db_name):
        if self.db_connector.db_type == 'sqlite':
            print("SQLite использует файлы, базы данных создаются автоматически.")
            return False

        try:
            self.cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"База данных '{db_name}' успешно создана.")
            return True
        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
            return False

    def create_table(self, table_name, schema):
        try:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
            self.connection.commit()
            print(f"Таблица '{table_name}' успешно создана.")
            return True
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")
            self.connection.rollback()
            return False

    def drop_table(self, table_name):
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.connection.commit()
            print(f"Таблица '{table_name}' успешно удалена.")
            return True
        except Exception as e:
            print(f"Ошибка при удалении таблицы: {e}")
            self.connection.rollback()
            return False

    def close(self):
        self.cursor.close()
        self.db_connector.close()
