import sqlite3
from .interfaces import IConnection


class Connection(IConnection):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_path: str):
        if not hasattr(self, 'db_path'): 
            self.db_path = db_path
            self.connection = None

    def connect(self) -> sqlite3.Connection:
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            
    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
