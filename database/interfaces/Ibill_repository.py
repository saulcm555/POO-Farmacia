from abc import ABC, abstractmethod

class IBillRepository(ABC):
    def obtener_factura(self, id_factura: int):
        pass
    