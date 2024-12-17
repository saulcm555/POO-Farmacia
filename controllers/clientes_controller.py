from models.cliente import Cliente

class ClientesController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def listar_clientes(self):
        users = self.db_manager.user_repo.listar_usuarios(role='cliente')
        return [Cliente(u['id_persona'], u['nombre'], u['telefono'], u['email'], u['direccion']) for u in users]
    
    def listar_empleados(self):
        users = self.db_manager.user_repo.listar_usuarios(role='admin')
        return [Cliente(u['id_persona'], u['nombre'], u['telefono'], u['email'], u['direccion']) for u in users]
