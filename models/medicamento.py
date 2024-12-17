from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para clases abstractas

class Medicamento(ABC):  # Clase abstracta Medicamento
    def __init__(self, codigo, nombre, proveedor, precio, fecha_caducidad, stock):
        self._codigo = codigo  # Código único del medicamento
        self._nombre = nombre.strip().lower()  # Nombre en minúsculas sin espacios extra
        self.proveedor = proveedor  # Proveedor del medicamento
        self._precio = precio  # Precio base del medicamento (atributo protegido)
        self.fecha_caducidad = fecha_caducidad  # Fecha de caducidad
        self.stock = stock  # Cantidad en stock

    @abstractmethod
    def calcular_precio_venta(self):  # Método abstracto para calcular precio de venta
        pass

    def obtener_datos(self):  # Método para obtener los datos del medicamento
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "proveedor": self.proveedor,
            "precio": self._precio,  # Precio base
            "fecha_caducidad": self.fecha_caducidad,
            "stock": self.stock,
        }

    def actualizar_stock(self, cantidad):  # Método para actualizar el stock
        self.stock += cantidad

    def __str__(self):  # Representación en cadena del medicamento
        return f"{self._nombre.capitalize()} - Código: {self._codigo} - Stock: {self.stock}"


class MedicamentoGenerico(Medicamento):  # Clase para medicamentos genéricos
    def calcular_precio_venta(self):  # Método concreto: precio base * 1.2
        return self._precio * 1.2

    def __str__(self):  # Representación específica para medicamentos genéricos
        return f"Genérico: {super().__str__()}"


class MedicamentoMarca(Medicamento):  # Clase para medicamentos de marca
    def calcular_precio_venta(self):  # Método concreto: precio base * 1.5
        return self._precio * 1.5

    def __str__(self):  # Representación específica para medicamentos de marca
        return f"Marca: {super().__str__()}"
