from user_factory import UserFactory
class UsersController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def listar_clientes(self):
        users = self.db_manager.user_repo.listar_usuarios(role='cliente')
        return [UserFactory.create_user(u) for u in users]
    
    def listar_empleados(self):
        users = self.db_manager.user_repo.listar_usuarios(role='admin')
        return [UserFactory.create_user(u) for u in users]