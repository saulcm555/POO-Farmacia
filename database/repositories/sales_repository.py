from ..interfaces import ISalesRepository, ISQLOperations
from datetime import datetime
class SalesRepository(ISalesRepository):
    def __init__(self, db: ISQLOperations):
        self.db = db
        
    def obtener_venta(self, id_venta):
        query = "SELECT * FROM ventas WHERE id = ?"
        venta = self.db.execute_query(query, (id_venta,))
        return venta[0] if venta else None
    
    def eliminar_venta(self, id_venta):
        query = "DELETE FROM ventas WHERE id = ?"
        self.db.execute_query(query, (id_venta,))
        return True
    
    def realizar_venta(self, id_cliente, id_empleado, medicamentos):
        query = "INSERT INTO ventas (id_cliente, id_empleado, fecha, total) VALUES (?, ?, ?, ?)"
        values = (id_cliente, id_empleado, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sum(med._precio * cantidad for med, cantidad in medicamentos))
        self.db.execute_query(query, values)
        return True