class Proveedor:  # Clase para representar a un proveedor
    def __init__(self, id_proveedor, nombre, telefono, email, direccion):
        self.id_proveedor = id_proveedor  # Identificador único del proveedor
        self.nombre = nombre  # Nombre del proveedor
        self.telefono = telefono  # Teléfono de contacto
        self.email = email  # Correo electrónico del proveedor
        self.direccion = direccion  # Dirección del proveedor

    def suministrar(self, inventario, medicamento, cantidad):  # Método para suministrar medicamentos
        inventario.actualizar_stock(medicamento._codigo, cantidad)  # Actualiza el stock en el inventario

    def __str__(self):  # Método para representar al proveedor como cadena
        return f"Proveedor: {self.nombre} (ID: {self.id_proveedor})"  # Muestra nombre e ID del proveedor
