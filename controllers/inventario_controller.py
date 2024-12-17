# controllers/inventario_controller.py
from models.medicamento import MedicamentoGenerico, MedicamentoMarca


class InventoryController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def _obtener_datos_medicamento(self, medicamento):
        datos = medicamento.obtener_datos()
        codigo = datos["codigo"]
        nombre = datos["nombre"]
        proveedor = datos["proveedor"]
        precio = datos["precio"]
        fecha_caducidad = datos["fecha_caducidad"]
        stock = datos["stock"]
        return codigo, nombre, proveedor, precio, fecha_caducidad, stock

    def obtener_todos_medicamentos(self):
        filas = self.db_manager.medicine_repo.listar_medicamentos()
        medicamentos = self.convertir_a_medicamento(filas)
        return medicamentos

    def agregar_medicamento(self, medicamento):
        datos = self._obtener_datos_medicamento(medicamento)
        self.db_manager.medicine_repo.guardar_medicamento(*datos)

    def actualizar_medicamento(self, medicamento):
        datos = self._obtener_datos_medicamento(medicamento)
        print("INVENTORY CONTROLLER", datos)
        self.db_manager.medicine_repo.actualizar_medicamento(*datos)

    def eliminar_medicamento(self, codigo):
        self.db_manager.medicine_repo.eliminar_medicamento(codigo)

    def buscar_medicamento_similares(self, criterio):
        filas = self.db_manager.medicine_repo.buscar_medicamento_similaridades(criterio)
        
        medicamentos = self.convertir_a_medicamento(filas)
        return medicamentos
    
    def buscar_medicamento_por_codigo(self, codigo):
        fila = self.db_manager.medicine_repo.buscar_medicamento_por_codigo(codigo)
        if fila:
            medicamento = self.convertir_a_medicamento(fila)
            return medicamento[0]
        return None
    
    

    def convertir_a_medicamento(self, filas):
        medicamentos = []
        for fila in filas:
            print(f"Row data: {fila}")  # Log the row to inspect its content
            if len(fila) < 6:  # Check if the row has less than 6 columns
                print(f"Skipping row with insufficient data: {fila}")
                continue  # Skip rows with insufficient data
            medicamento = MedicamentoGenerico(
                codigo=fila[0],
                nombre=fila[1],
                proveedor=fila[2],
                precio=fila[3],
                fecha_caducidad=fila[4],
                stock=fila[5],
            )
            medicamentos.append(medicamento)
        return medicamentos
