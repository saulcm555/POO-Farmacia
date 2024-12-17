from ..interfaces import IBillRepository, ISQLOperations

class BillRepository(IBillRepository):
    def __init__(self, db: ISQLOperations):
        self.db = db
    
    def obtener_factura(self, id_factura):
        query = "SELECT * FROM facturas WHERE id = ?"
        factura = self.db.execute_query(query, (id_factura,))
        return factura[0] if factura else None
    