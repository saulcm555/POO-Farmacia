from .interfaces import ISalesService

from database.repositories import (
    SalesRepository,
    SalesDetailRepository,
    MedicineRepository,
)


class SalesService(ISalesService):
    def __init__(
        self,
        sales_repo: SalesRepository,
        medicine_repo: MedicineRepository,
        sales_detail_repo: SalesDetailRepository,
    ):
        self.sales_repo = sales_repo
        self.medicine_repo = medicine_repo
        self.sales_detail_repo = sales_detail_repo

    def anular_venta(self, venta_id):
        detalles_venta = self.sales_detail_repo.obtener_detalles_venta(venta_id)

        self.sales_repo.eliminar_venta(venta_id)
        self.sales_detail_repo.eliminar_detalles_venta(venta_id)

        for detalle in detalles_venta:
            self.medicine_repo.actualizar_stock_medicamento(
                detalle["codigo_medicamento"], detalle["cantidad"]
            )
