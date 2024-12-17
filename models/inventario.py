from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para clases abstractas

class Observador(ABC):  # Clase abstracta Observador
    @abstractmethod
    def actualizar(self, medicamento):  # Método abstracto que deben implementar los observadores
        pass

class InventarioObservable:  # Clase base para observables del inventario
    def __init__(self):
        self._observadores = []  # Lista para almacenar los observadores

    def agregar_observador(self, observador):  # Agrega un observador a la lista
        self._observadores.append(observador)

    def eliminar_observador(self, observador):  # Elimina un observador de la lista
        self._observadores.remove(observador)

    def notificar_observadores(self, medicamento):  # Notifica a todos los observadores
        for observador in self._observadores:
            observador.actualizar(medicamento)

class Inventario(InventarioObservable):  # Clase Inventario que hereda de InventarioObservable
    def __init__(self):
        super().__init__()  # Inicializa la clase base
        self.medicamentos = {}  # Diccionario para almacenar medicamentos por código

    def agregar_medicamento(self, medicamento):  # Agrega un medicamento al inventario
        self.medicamentos[medicamento._codigo] = medicamento
        self.notificar_observadores(medicamento)  # Notifica a los observadores

    def eliminar_medicamento(self, codigo):  # Elimina un medicamento por código
        if codigo in self.medicamentos:
            medicamento = self.medicamentos.pop(codigo)
            self.notificar_observadores(medicamento)  # Notifica a los observadores

    def actualizar_stock(self, codigo, cantidad):  # Actualiza el stock de un medicamento
        if codigo in self.medicamentos:
            self.medicamentos[codigo].actualizar_stock(cantidad)  # Actualiza el stock del medicamento
            self.notificar_observadores(self.medicamentos[codigo])  # Notifica a los observadores

    def buscar_medicamento(self, criterio):  # Busca medicamentos por nombre o criterio
        return [med for med in self.medicamentos.values() if criterio.lower() in med._nombre.lower()]

    def obtener_medicamento(self, codigo):  # Obtiene un medicamento por su código
        return self.medicamentos.get(codigo)

    def __str__(self):  # Método para representar el inventario como cadena
        return f"Inventario: {len(self.medicamentos)} medicamentos"  # Muestra cantidad total de medicamentos
