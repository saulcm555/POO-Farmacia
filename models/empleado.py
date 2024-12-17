from models.persona import Persona  # Importa la clase base Persona desde models.persona

class Empleado(Persona):  # Clase Empleado que hereda de Persona
    def __init__(self, id_persona, nombre, telefono, email, direccion, cargo, salario):
        super().__init__(id_persona, nombre, telefono, email, direccion)  # Inicializa atributos heredados
        self.cargo = cargo  # Asigna el cargo del empleado
        self.salario = salario  # Asigna el salario del empleado

    def obtener_tipo(self):  # Método para identificar el tipo de persona
        return "Empleado"  # Retorna la cadena "Empleado"

    def __str__(self):  # Método para representar el objeto como una cadena
        return f"{super().__str__()} - Cargo: {self.cargo}"  # Incluye información heredada y el cargo
