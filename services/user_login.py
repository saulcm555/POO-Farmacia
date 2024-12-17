from models.cliente import Cliente
from models.empleado import Empleado
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

        if user_data and user_data['password'] == hashed_password:
            self.user = self._create_user_object(user_data)
            return self.user
        return None

    def _hash_password(self, password):
        return password  # Simulación para el ejemplo

    def _create_user_object(self, user_data):
        if user_data['role'] == 'admin':
            return Empleado(
                id_persona=user_data['id_persona'],
                nombre=user_data['nombre'],
                telefono=user_data['telefono'],
                email=user_data['email'],
                direccion=user_data['direccion'],
                cargo="Ventas",
                salario=1000
            )
        else:
            return Cliente(
                id_persona=user_data['id_persona'],
                nombre=user_data['nombre'],
                telefono=user_data['telefono'],
                email=user_data['email'],
                direccion=user_data['direccion']

            )

    def get_current_user(self):
        return self.user
