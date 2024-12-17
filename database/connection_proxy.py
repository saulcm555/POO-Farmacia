from .interfaces import IConnection

class ConnectionProxy(IConnection):
    def __init__(self, real_connection):
        self.real_connection = real_connection

    def connect(self):
        print("Estableciendo conexión a través del proxy...")
        return self.real_connection.connect()

    def close(self):
        print("Cerrando conexión a través del proxy...")
        self.real_connection.close()

    def cursor(self):
        print("Obteniendo cursor a través del proxy...")
        return self.real_connection.cursor()

    def commit(self):
        print("Confirmando cambios a través del proxy...")
        self.real_connection.commit()

    def __enter__(self):
        print("Iniciando conexión con el contexto del proxy...")
        return self.real_connection.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Finalizando conexión con el contexto del proxy...")
        self.real_connection.__exit__(exc_type, exc_val, exc_tb)
