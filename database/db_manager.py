from .interfaces import IConnection, ISQLOperations
from .interfaces import (
    IUserRepository,
    ISalesRepository,
    IMedicineRepository,
)


class DatabaseManager:
    def __init__(
        self,
        db_connection: IConnection,
        operations: ISQLOperations,
        
        user_repo: IUserRepository,
        sales_repo: ISalesRepository,
        medicine_repo: IMedicineRepository,
    ):
        self.db_connection = db_connection
        self.connection = self.db_connection.connect()
        self.operations = operations

        self.user_repo = user_repo
        self.sales_repo = sales_repo
        self.medicine_repo = medicine_repo
        self.initialize()

    def close(self):
        self.db_connection.close()

    def initialize(self):
        self._create_tables()
        self.user_repo.create_default_users()

    def _create_tables(self):
        RUTA_SQL = r"database/sql_creation_tables.sql"

        with open(RUTA_SQL, "r") as file:
            tables_query = file.read()

        # Ejecutar las consultas separadas en el archivo SQL
        self.operations.execute_query(tables_query)
