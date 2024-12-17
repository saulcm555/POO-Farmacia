from datetime import datetime  # Importa datetime para registrar la fecha y hora

class Venta:  # Clase para representar una venta
    def __init__(self, id_venta, cliente, empleado, medicamentos, total):
        self.id_venta = id_venta  # Identificador único de la venta
        self.cliente = cliente  # Objeto cliente asociado a la venta
        self.empleado = empleado  # Objeto empleado que realizó la venta
        self.medicamentos = medicamentos  # Lista de medicamentos vendidos (con cantidades)
        self.total = total  # Total de la venta
        self.fecha = datetime.now()  # Fecha y hora actual de la venta

    def __str__(self):  # Método para representar la venta como cadena
        return f"Venta #{self.id_venta} - Cliente: {self.cliente.nombre} - Total: ${self.total:.2f} - Fecha: {self.fecha}"
        # Muestra ID, nombre del cliente, total y fecha de la venta
