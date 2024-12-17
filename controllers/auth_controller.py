from models.persona import Persona

class AuthController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def login(self, username, password):
        hashed_password = self._hash_password(password)
        user = self.db_manager.user_repo.get_user(username)[0]
        if user and user['password'] == hashed_password:
            return self._create_user_object(user)
        return None
    
    def logout(self):
        pass

        
    def register(self, username, password, role, telefono=None, email=None, direccion=None):
        hashed_password = self._hash_password(password)
        user_id = self.db_manager.user_repo.create_user(username=username, password=hashed_password, role=role, telefono=telefono, email=email, direccion=direccion)
        return self.db_manager.user_repo.get_user(username)

    def _hash_password(self, password):
        return password

    def _create_user_object(self, user_data):
        if user_data['role'] == 'cliente':
            from models.cliente import Cliente
            return Cliente(user_data['id_persona'], user_data['nombre'], user_data['telefono'],
                           user_data['email'], user_data['direccion'])
        elif user_data['role'] == 'admin':
            from models.empleado import Empleado
            return Empleado(user_data['id_persona'], user_data['nombre'], user_data['telefono'],
                            user_data['email'], user_data['direccion'], 'Administrador', None)
        else:
            return Persona(user_data['id_persona'], user_data['nombre'], user_data['telefono'],
                           user_data['email'], user_data['direccion'])
            
            
            
            
            