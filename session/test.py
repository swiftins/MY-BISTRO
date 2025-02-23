class UsersSession:
    def __init__(self):
        self._user_sessions = {}

    def __getitem__(self, key):
        print(f"Попытка доступа к элементу с ключом: {key}")
        return self.get(key)

    def __setitem__(self, key, value):
        print(f"Попытка установить значение для ключа {key}: {value}")
        self._user_sessions[key] = value

    def __delitem__(self, key):
        print(f"Попытка удалить элемент с ключом: {key}")
        del self._user_sessions[key]

    def get(self, user_id):
        if user_id not in self._user_sessions:
            self._user_sessions[user_id] = Session(user_id)
        return self._user_sessions[user_id]

    def get_order(self, user_id):
        return self.get(user_id).get()


class Session:
    def __init__(self, user_id):
        self.user_id = user_id

    def get(self):
        return f"Order for user {self.user_id}"


if __name__ == "__main__":
    session = UsersSession()

    # Используем индексатор для доступа к user_sessions через класс
    session['shape'] = 'Shape value'  # Вызовет __setitem__

    print(session['shape'])  # Вызовет __getitem__

    del session['shape']  # Вызовет __delitem__
