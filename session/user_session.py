from order_manager import init_fo_manager
class UsersSession:
    def __init__(self):
        self._user_sessions = {}

    def __getitem__(self, key):
        print(f"Попытка доступа к элементу с ключом: {key}")
        if key not in self._user_sessions:
            print(f"Ключ {key} отсутствует. Создаю новый объект.")
            self._user_sessions[key] = Session(key)
        return self._user_sessions[key]

    def __setitem__(self, key, value):
        print(f"Попытка установить значение для ключа {key}: {value}")
        self._user_sessions[key] = value

    def __delitem__(self, key):
        print(f"Попытка удалить элемент с ключом: {key}")
        del self._user_sessions[key]

    # def __getattr__(self, item):
    #     print(item)
    #     return self.user_sessions


    # def get(self,user_id):
    #     if user_id not in self._user_sessions:
    #         self._user_sessions[user_id] = Session(user_id)
    #     return self._user_sessions[user_id]
    #
    # def get_order(self,user_id):
    #     return self.get(user_id).get()


class Session:
    def __init__(self, user_id):
        self.user_id = user_id
        self.order_id = None
        self.step = None
        self.messages = []
        self.order_form = None

        food_order_manager = init_fo_manager()
        print("Вызов __init__ класса Session")
        if food_order_manager.check_user_exists(telegram_id=self.user_id):
            pending_order = food_order_manager.get_user_orders_by_status(self.user_id)
            if len(pending_order)>0:
                pending_order = pending_order[-1]
                if pending_order:
                    self.order_id = pending_order[0]


        food_order_manager.db_manager.close()

    def __getitem__(self, key):
        if not hasattr(self, key):
            setattr(self, key, None)
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        # Удаляем атрибут с заданным именем
        if hasattr(self, key):
            delattr(self, key)
        else:
            print(f"Нет атрибута с именем {key} для удаления.")

    def update(self, attributes):
        """Метод для обновления нескольких атрибутов из словаря."""
        for key, value in attributes.items():
            self[key] = value  # Используем __setitem__ для добавления атрибутов

    def get(self, key):
        if not hasattr(self, key):
            setattr(self, key, None)
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)

if __name__ == "__main__":
    session = UsersSession()


    print(session[708479119]["order_id"])

    #print(session.get(708479119))

    #print(session.get(708479119).get("order_id"))
