from abc import ABC, abstractmethod

class ISalesService: 
    @abstractmethod
    def anular_venta(self, venta_id: int):
        pass