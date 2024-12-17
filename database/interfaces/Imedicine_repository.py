from abc import ABC, abstractmethod

class IMedicineRepository(ABC):
    @abstractmethod
    def listar_medicamentos(self):
        pass
    
    @abstractmethod
    def guardar_medicamento(self, codigo, nombre, proveedor, precio, fecha_caducidad, stock):
        pass
    
    @abstractmethod
    def actualizar_medicamento(self, codigo, nombre, precio, stock, descripcion, laboratorio):
        pass
    
    @abstractmethod
    def eliminar_medicamento(self, codigo):
        pass
    
    @abstractmethod
    def buscar_medicamento_similaridades(self, criterio):
        pass
    
    @abstractmethod
    def actualizar_stock_medicamento(self, codigo_medicamento: str, cantidad: int):
        pass