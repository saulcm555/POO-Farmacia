from models.empleado import Empleado

class EmpleadosController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def agregar_empleado(self, nombre, telefono, email, direccion, cargo, salario):
        empleado = Empleado(None, nombre, telefono, email, direccion, cargo, salario)
        return self.db_manager.guardar_usuario(empleado)

    def obtener_empleado(self, id_empleado):
        user_data = self.db_manager.obtener_usuario(id_empleado)
        if user_data and user_data['role'] == 'admin':
            return Empleado(user_data['id_persona'], user_data['nombre'], user_data['telefono'], 
                            user_data['email'], user_data['direccion'], user_data['cargo'], user_data['salario'])
        return None

    def actualizar_empleado(self, id_empleado, nombre, telefono, email, direccion, cargo, salario):
        empleado = self.obtener_empleado(id_empleado)
        if empleado:
            empleado.nombre = nombre
            empleado.telefono = telefono
            empleado.email = email
            empleado.direccion = direccion
            empleado.cargo = cargo
            empleado.salario = salario
            return self.db_manager.actualizar_usuario(empleado)
        return False

    def eliminar_empleado(self, id_empleado):
        return self.db_manager.eliminar_usuario(id_empleado)

    def listar_empleados(self):
        users = self.db_manager.listar_usuarios(role='admin')
        return [Empleado(u['id_persona'], u['nombre'], u['telefono'], u['email'], u['direccion'], u['cargo'], u['salario']) for u in users]