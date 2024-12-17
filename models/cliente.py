from models.persona import Persona  # Importa la clase base Persona desde models.persona

class Cliente(Persona):  # Clase Cliente que hereda de Persona
    def __init__(self, id_persona, nombre, telefono, email, direccion, puntos_fidelidad=0):
        super().__init__(id_persona, nombre, telefono, email, direccion)  # Inicializa atributos heredados
        self.puntos_fidelidad = puntos_fidelidad  # Inicializa puntos de fidelidad del cliente

    def obtener_tipo(self):  # Método para identificar el tipo de persona
        return "Cliente"  # Retorna la cadena "Cliente"

    def agregar_puntos(self, puntos):  # Método para agregar puntos de fidelidad
        self.puntos_fidelidad += puntos  # Suma los puntos a los existentes

    def __str__(self):  # Método para representar el objeto como una cadena
        return f"{super().__str__()} - Puntos: {self.puntos_fidelidad}"  # Incluye información heredada y puntos
