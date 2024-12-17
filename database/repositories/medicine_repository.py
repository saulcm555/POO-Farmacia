from ..interfaces import IMedicineRepository, ISQLOperations

class MedicineRepository(IMedicineRepository):
    def __init__(self, db: ISQLOperations):
        self.db = db

    def listar_medicamentos(self):
        query = "SELECT * FROM medicamentos"
        medicamentos = self.db.execute_query(query)
        return medicamentos[0]

    def guardar_medicamento(self, codigo, nombre, proveedor, precio, fecha_caducidad, stock):
        query = "INSERT INTO medicamentos VALUES (?, ?, ?, ?, ?, ?)"
        values = (codigo, nombre, proveedor, precio, fecha_caducidad, stock)
        self.db.execute_query(query, values)
        return True

    def actualizar_medicamento(self, codigo, nombre, proveedor, precio, fecha_caducidad, stock):
        query = "UPDATE medicamentos SET nombre = ?, proveedor = ?, precio = ?, fecha_caducidad = ?, stock = ? WHERE codigo = ?"
        values = (nombre, proveedor, precio, fecha_caducidad, stock, codigo)
        self.db.execute_query(query, values)
        return True

    def eliminar_medicamento(self, codigo):
        query = "DELETE FROM medicamentos WHERE codigo = ?"
        self.db.execute_query(query, (codigo,))
        return True

    def buscar_medicamento_similaridades(self, criterio):
        query = "SELECT * FROM medicamentos WHERE codigo LIKE ? OR nombre LIKE ?"
        wildcard_criterio = f"%{criterio}%"
        medicamentos = self.db.execute_query(query, (wildcard_criterio, wildcard_criterio))
        return medicamentos[0]

    def buscar_medicamento_por_codigo(self, codigo):
        query = "SELECT * FROM medicamentos WHERE codigo = ?"
        medicamento = self.db.execute_query(query, (codigo,))
        return medicamento[0]

    def actualizar_stock_medicamento(self, codigo_medicamento: str, cantidad: int):
        query = "UPDATE medicamentos SET stock = stock - ? WHERE codigo = ?"
        self.db.execute_query(query, (cantidad, codigo_medicamento))
        return True

    def buscar_medicamento(self, codigo: str):
        query = "SELECT * FROM medicamentos WHERE codigo = ?"
        medicamento = self.db.execute_query(query, (codigo,))
        return medicamento[0]
