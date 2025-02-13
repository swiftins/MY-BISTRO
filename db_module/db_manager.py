class DBManager:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        self.connection = db_connector.get_connection()
        self.cursor = self.connection.cursor()

    def fetch_data(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False

    def insert_data(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Ошибка при вставке данных: {e}")
            self.connection.rollback()
            return False

    def update_data(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            self.connection.rollback()
            return False

    def delete_data(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Ошибка при удалении данных: {e}")
            self.connection.rollback()
            return False

    def close(self):
        self.cursor.close()
        self.db_connector.close()
