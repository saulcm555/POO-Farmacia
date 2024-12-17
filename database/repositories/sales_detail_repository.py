from ..interfaces import ISalesDetailRepository, ISQLOperations

class SalesDetailRepository(ISalesDetailRepository):
    def __init__(self, db: ISQLOperations):
        self.db = db
    
    def obtener_detalles_venta(self, id_venta):
        query = "SELECT * FROM detalle_ventas WHERE id_venta = ?"
        detalle_venta = self.db.execute_query(query, (id_venta,))
        return detalle_venta

    def eliminar_detalles_venta(self, id_detalle_venta):
        query = "DELETE FROM detalle_ventas WHERE id = ?"
        self.db.execute_query(query, (id_detalle_venta,))
        return True
