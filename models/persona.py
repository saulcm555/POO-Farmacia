from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para clases abstractas

class Persona(ABC):  # Clase abstracta base Persona
    def __init__(self, id_persona, nombre, telefono, email, direccion):
        self.id_persona = id_persona  # Identificador único de la persona
        self.nombre = nombre  # Nombre de la persona
        self.telefono = telefono  # Teléfono de contacto
        self.email = email  # Correo electrónico
        self.direccion = direccion  # Dirección de la persona

    @abstractmethod
    def obtener_tipo(self):  # Método abstracto para definir el tipo de persona
        pass

    def __str__(self):  # Método para representar la persona como cadena
        return f"{self.obtener_tipo()}: {self.nombre} (ID: {self.id_persona})"  
        # Muestra tipo de persona, nombre e ID
