from models.cliente import Cliente
from models.empleado import Empleado
from models.persona import Persona

class UserFactory:
    @staticmethod
    def create_user(user_data):
        """
        Factory method to create user objects based on role.
        :param user_data: dict containing user information, including 'role'.
        :return: An instance of Cliente, Empleado, or Persona.
        """
        user_data = dict(user_data)
        role = user_data.get('role')
        
        if role == 'cliente':
            return Cliente(
                user_data['id_persona'], 
                user_data['nombre'], 
                user_data['telefono'],
                user_data['email'], 
                user_data['direccion']
            )
        elif role == 'admin':
            return Empleado(
                user_data['id_persona'], 
                user_data['nombre'], 
                user_data['telefono'],
                user_data['email'], 
                user_data['direccion'], 
                'Administrador', 
                None
            )
        else:
            return Persona(
                user_data['id_persona'], 
                user_data['nombre'], 
                user_data['telefono'],
                user_data['email'], 
                user_data['direccion']
            )
