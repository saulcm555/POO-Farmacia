from datetime import datetime  # Importa la clase datetime para manejar fechas y horas

class Factura:
    def __init__(self, id_factura, venta):
        self.id_factura = id_factura  # Asigna el identificador de la factura
        self.venta = venta  # Asigna la venta asociada a la factura
        self.fecha_emision = datetime.now()  # Registra la fecha y hora actual de emisión

    def generar_factura(self):  # Método para generar la representación de la factura
        # Genera una lista de detalles de productos en la venta
        detalles = [
            f"Producto: {med._nombre}, Cantidad: {cant}, Precio: {med.calcular_precio_venta()}"
            for med, cant in self.venta.medicamentos  # Itera sobre medicamentos y cantidades
        ]
        # Retorna la factura formateada con detalles del cliente, empleado y total
        return f"""
        Factura #{self.id_factura}
        Fecha: {self.fecha_emision}
        Cliente: {self.venta.cliente.nombre}
        Empleado: {self.venta.empleado.nombre}
        
        Detalles:
        {chr(10).join(detalles)}  # Junta los detalles en líneas separadas
        
        Total: ${self.venta.total:.2f}  # Muestra el total con dos decimales
        """

    def __str__(self):  # Método para representar la factura como cadena
        return f"Factura #{self.id_factura} - Venta ID: {self.venta.id_venta} - Fecha: {self.fecha_emision}"
        # Incluye ID de factura, ID de venta y fecha de emisión
