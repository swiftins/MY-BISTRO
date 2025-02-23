class UsersSession:
    def __init__(self):
        self.user_sessions = {}

    def __getitem__(self, key):
        print(f"Попытка доступа к элементу с ключом: {key}")
        return self.get(key)

    def __setitem__(self, key, value):
        print(f"Попытка установить значение для ключа {key}: {value}")
        self.user_sessions[key] = value

    def __delitem__(self, key):
        print(f"Попытка удалить элемент с ключом: {key}")
        del self.user_sessions[key]

    def get(self, user_id):
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = Session(user_id)
        return self.user_sessions[user_id]

    def get_order(self, user_id):
        return self.get(user_id).get()


class Session:
    def __init__(self, user_id):
        self.user_id = user_id

    def get(self):
        return f"Order for user {self.user_id}"


if __name__ == "__main__":
    session = UsersSession()

    # Теперь мы можем использовать индексатор для словаря
    session.user_sessions['shape'] = 'Shape value'  # Вызовет __setitem__

    print(session.user_sessions['shape'])  # Вызовет __getitem__

    del session.user_sessions['shape']  # Вызовет __delitem__
