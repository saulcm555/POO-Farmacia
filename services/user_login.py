from user_factory import UserFactory


class UserLogin:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_manager):
        if not hasattr(self, "user"):
            self.user = None
        if not hasattr(self, "db_manager"):
            self.db_manager = db_manager

    def login(self, username, password):
        hashed_password = self._hash_password(password)
        user_data = self.db_manager.user_repo.get_user(username)

        if user_data and user_data["password"] == hashed_password:
            self.user = UserFactory.create_user(user_data)
            return self.user
        return None

    def _hash_password(self, password):
        return password  # Simulación para el ejemplo

    def get_current_user(self):
        return self.user
