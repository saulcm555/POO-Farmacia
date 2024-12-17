from abc import ABC, abstractmethod

class ISalesDetailRepository(ABC):
    @abstractmethod
    def obtener_detalles_venta(self, id_detalle_venta: int) :
        pass
    
    @abstractmethod
    def eliminar_detalles_venta(self, id_detalle_venta: int) :
        pass