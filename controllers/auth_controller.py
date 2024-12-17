from user_factory import UserFactory

class AuthController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def login(self, username, password):
        hashed_password = self._hash_password(password)
        user = self.db_manager.user_repo.get_user(username)[0]
        if user and user['password'] == hashed_password:
            return UserFactory.create_user(user)
        return None
    
    def logout(self):
        pass

        
    def register(self, username, password, role, telefono=None, email=None, direccion=None):
        hashed_password = self._hash_password(password)
        user_id = self.db_manager.user_repo.create_user(username=username, password=hashed_password, role=role, telefono=telefono, email=email, direccion=direccion)
        return self.db_manager.user_repo.get_user(username)

    def _hash_password(self, password):
        return password

