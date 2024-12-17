from .interfaces import IConnection  # Importa la interfaz IConnection

class ConnectionProxy(IConnection):  # Clase proxy que implementa IConnection
    def __init__(self, real_connection):
        self.real_connection = real_connection  # Almacena la conexión real a la base de datos

    def connect(self):  # Método para establecer conexión
        print("Estableciendo conexión a través del proxy...")
        return self.real_connection.connect()  # Delega la conexión a la real_connection

    def close(self):  # Método para cerrar la conexión
        print("Cerrando conexión a través del proxy...")
        self.real_connection.close()  # Cierra la conexión real

    def cursor(self):  # Método para obtener un cursor
        print("Obteniendo cursor a través del proxy...")
        return self.real_connection.cursor()  # Devuelve el cursor de la real_connection

    def commit(self):  # Método para confirmar cambios
        print("Confirmando cambios a través del proxy...")
        self.real_connection.commit()  # Confirma cambios en la real_connection

    def __enter__(self):  # Método para el inicio de un contexto (with statement)
        print("Iniciando conexión con el contexto del proxy...")
        return self.real_connection.__enter__()  # Delegación al método __enter__

    def __exit__(self, exc_type, exc_val, exc_tb):  # Método para finalizar el contexto
        print("Finalizando conexión con el contexto del proxy...")
        self.real_connection.__exit__(exc_type, exc_val, exc_tb)  # Delegación al método __exit__
