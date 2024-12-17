from database import DatabaseManager, Connection, SQLOperations
from database.repositories import (
    UserRepository,
    MedicineRepository,
    BillRepository,
    SalesDetailRepository,
    SalesRepository,
)


from utils.notifications import Notifications
from controllers.auth_controller import AuthController
from controllers.inventario_controller import InventoryController
from controllers.ventas_controller import VentasController
from controllers.clientes_controller import ClientesController
from services.user_login import UserLogin

DB_PATH = r"farmacia.db"


class DependencyInjector:
    def __init__(self):
        self.repositories = {}
        self.controllers = {}
        self.connection = Connection(DB_PATH)
        self.sql_operations = SQLOperations(self.connection)
        self._initialize_repositories()

        # Database Manager
        self.db_manager = DatabaseManager(
            self.connection,
            self.sql_operations,
            user_repo=self.get_repo("user_repository"),
            medicine_repo=self.get_repo("medicine_repository"),
            bill_repo=self.get_repo("bill_repository"),
            sales_detail_repo=self.get_repo("sales_detail_repository"),
            sales_repo=self.get_repo("sales_repository"),
        )

        self._initialize_controllers()

    def _initialize_repositories(self):
        self._register_repository(
            "user_repository", UserRepository(self.sql_operations)
        )
        self._register_repository(
            "medicine_repository", MedicineRepository(self.sql_operations)
        )
        self._register_repository(
            "bill_repository", BillRepository(self.sql_operations)
        )
        self._register_repository(
            "sales_detail_repository", SalesDetailRepository(self.sql_operations)
        )
        self._register_repository(
            "sales_repository", SalesRepository(self.sql_operations)
        )

    def _initialize_controllers(self):
        self._register_controller("auth_controller", AuthController(self.db_manager))
        self._register_controller(
            "inventory_controller",
            InventoryController(self.db_manager),
        )
        self._register_controller("notifications", Notifications())
        self._register_controller("ventas_controller", VentasController(self.db_manager))
        self._register_controller("clientes_controller", ClientesController(self.db_manager))
        self._register_controller("user_login", UserLogin(self.db_manager))


    def _register_repository(self, name, repository):
        if name in self.repositories:
            raise ValueError(f"El repositorio '{name}' ya está registrado.")
        self.repositories[name] = repository

    def _register_controller(self, name, controller):
        if name in self.controllers:
            raise ValueError(f"El controlador '{name}' ya está registrado.")
        self.controllers[name] = controller

    def get_repo(self, name):
        if name not in self.repositories:
            raise KeyError(f"El repositorio '{name}' no está registrado.")
        return self.repositories[name]

    def get_controller(self, name):
        if name not in self.controllers:
            raise KeyError(f"El controlador '{name}' no está registrado.")
        return self.controllers[name]
