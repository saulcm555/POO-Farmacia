from models.factura import Factura
from models.medicamento import MedicamentoGenerico, MedicamentoMarca

class VentasController:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Utilizar el objeto de gestión de la base de datos
    def realizar_venta(self, id_cliente, id_empleado, medicamentos):
        # Calcular el total de la venta
        total = sum(med.calcular_precio_venta() * cantidad for med, cantidad in medicamentos)
        
        # Actualizar el stock para cada medicamento
        for medicamento, cantidad in medicamentos:
            self.actualizar_stock(medicamento._codigo, -cantidad)

        # Realizar la venta en la base de datos
        self.db_manager.sales_repo.realizar_venta(id_cliente=id_cliente, id_empleado=id_empleado, medicamentos=medicamentos)
        return 

    def actualizar_stock(self, codigo_medicamento, cantidad):
        # Buscamos el medicamento por su código
        medicamento = self.db_manager.medicine_repo.buscar_medicamento_por_codigo(codigo_medicamento)
        
        if medicamento:
            # Si 'medicamento' es una lista, obtén el primer elemento
            if isinstance(medicamento, list):
                medicamento = medicamento[0]
            
            # Ahora accedes a los datos del medicamento correctamente
            medicamento = MedicamentoMarca(
                medicamento["codigo"], 
                medicamento["nombre"], 
                medicamento["proveedor"], 
                int(medicamento["precio"]), 
                medicamento["fecha_caducidad"], 
                medicamento["stock"]
            )
            
            # Ajusta el stock
            nuevo_stock = medicamento.stock + cantidad  # Suma el nuevo stock
            if nuevo_stock >= 0:  # Si el stock es positivo, actualiza el stock en la base de datos
                medicamento.actualizar_stock(cantidad)
                self.db_manager.medicine_repo.actualizar_medicamento(codigo=medicamento._codigo, nombre=medicamento._nombre, proveedor=medicamento.proveedor, precio=medicamento._precio, fecha_caducidad=medicamento.fecha_caducidad, stock=medicamento.stock)
                if medicamento.stock == 0:
                    self.db_manager.medicine_repo.eliminar_medicamento(codigo=medicamento._codigo)
            else:
                raise ValueError(f"Stock insuficiente para el medicamento {medicamento._nombre}")
        else:
            raise ValueError(f"Medicamento con código {codigo_medicamento} no encontrado")
