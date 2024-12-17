from abc import ABC, abstractmethod

class ISalesRepository(ABC):
    @abstractmethod
    def obtener_venta(self, id_venta: int) :
        pass
    
    @abstractmethod
    def eliminar_venta(self, id_venta: int) :
        pass
