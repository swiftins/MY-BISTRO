from order_manager import init_fo_manager
class UsersSession:
    def __init__(self):
        self.user_sessions = {}

    def get(self,user_id):
        self.user_sessions[user_id] = self.user_sessions.get(user_id,Session(user_id))
        return self.user_sessions[user_id]

    def get_order(self,user_id):
        session = self.get(user_id)


class Session:
    def __init__(self, user_id):
        self.user_id = user_id
        self.order_id = None
        self.step = None
        self.messages = []
        self.order_form = None

        food_order_manager = init_fo_manager()
        if food_order_manager.check_user_exists(telegram_id=self.user_id):
            pending_order = food_order_manager.get_user_orders_by_status(self.user_id)[-1]
            if pending_order:
                self.order_id = pending_order[0]

        food_order_manager.db_manager.close()

    def get(self, key):
        if not hasattr(self, key):
            setattr(self, key, None)
        return getattr(self, key)

    def set(self, key, value):
        setattr(self, key, value)

if __name__ == "__main__":
    session = UsersSession()

    print(session.get(708479119))

    print(session.get(708479119).get("order_id"))
