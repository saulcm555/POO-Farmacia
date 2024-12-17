from models.proveedor import Proveedor

class ProveedoresController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def agregar_proveedor(self, nombre, telefono, email, direccion):
        proveedor = Proveedor(None, nombre, telefono, email, direccion)
        return self.db_manager.guardar_proveedor(proveedor)

    def obtener_proveedor(self, id_proveedor):
        return self.db_manager.obtener_proveedor(id_proveedor)

    def actualizar_proveedor(self, id_proveedor, nombre, telefono, email, direccion):
        proveedor = self.obtener_proveedor(id_proveedor)
        if proveedor:
            proveedor.nombre = nombre
            proveedor.telefono = telefono
            proveedor.email = email
            proveedor.direccion = direccion
            return self.db_manager.actualizar_proveedor(proveedor)
        return False

    def eliminar_proveedor(self, id_proveedor):
        return self.db_manager.eliminar_proveedor(id_proveedor)

    def listar_proveedores(self):
        return self.db_manager.listar_proveedores()