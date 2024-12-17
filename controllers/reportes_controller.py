from datetime import datetime

class ReportesController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def generar_reporte_ventas(self, fecha_inicio, fecha_fin):
        ventas = self.db_manager.obtener_ventas(fecha_inicio, fecha_fin)
        total_ventas = sum(venta['total'] for venta in ventas)
        return {
            'ventas': ventas,
            'total_ventas': total_ventas,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def generar_reporte_inventario(self):
        inventario = self.db_manager.listar_medicamentos()
        valor_total = sum(med['precio'] * med['stock'] for med in inventario)
        return {
            'inventario': inventario,
            'valor_total': valor_total,
            'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def generar_reporte_medicamentos_bajos_stock(self, umbral=10):
        medicamentos = self.db_manager.listar_medicamentos()
        bajos_stock = [med for med in medicamentos if med['stock'] <= umbral]
        return {
            'medicamentos_bajos_stock': bajos_stock,
            'umbral': umbral,
            'fecha_generacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }