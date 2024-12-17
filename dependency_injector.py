from database import DatabaseManager, Connection, SQLOperations, ConnectionProxy
from database.repositories_strategy import (
    UserRepositoryStrategy,
    MedicineRepositoryStrategy,
    SalesRepositoryStrategy,
)
from controllers.controllers_strategy import (
    AuthControllerStrategy,
    InventoryControllerStrategy,
    NotificationsStrategy,
    VentasControllerStrategy,
    ClientesControllerStrategy,
    UserLoginStrategy,
)

DB_PATH = r"farmacia.db"


class DependencyInjector:
    def __init__(self):
        self.repositories = {}
        self.controllers = {}

        # Creación de la conexión y operaciones SQL
        self.real_connection = Connection(DB_PATH)
        self.connection = ConnectionProxy(self.real_connection)
        self.sql_operations = SQLOperations(self.connection)

        # Inicialización de las estrategias
        self._initialize_repository_strategies()
        self._initialize_controller_strategies()

        # Database Manager
        self.db_manager = DatabaseManager(
            self.connection,
            self.sql_operations,
            user_repo=self.get_repo("user_repository"),
            medicine_repo=self.get_repo("medicine_repository"),
            sales_repo=self.get_repo("sales_repository"),
        )

    def _initialize_repository_strategies(self):
        # Registro de estrategias de repositorios
        self._register_repository_strategy("user_repository", UserRepositoryStrategy())
        self._register_repository_strategy(
            "medicine_repository", MedicineRepositoryStrategy()
        )

        self._register_repository_strategy(
            "sales_repository", SalesRepositoryStrategy()
        )

    def _initialize_controller_strategies(self):
        # Registro de estrategias de controladores
        self._register_controller_strategy("auth_controller", AuthControllerStrategy())
        self._register_controller_strategy(
            "inventario_controller", InventoryControllerStrategy()
        )
        self._register_controller_strategy("notifications", NotificationsStrategy())
        self._register_controller_strategy(
            "ventas_controller", VentasControllerStrategy()
        )
        self._register_controller_strategy(
            "clientes_controller", ClientesControllerStrategy()
        )
        self._register_controller_strategy("user_login", UserLoginStrategy())

    def _register_repository_strategy(self, name, repository_strategy):
        if name in self.repositories:
            raise ValueError(f"El repositorio '{name}' ya está registrado.")
        self.repositories[name] = repository_strategy

    def _register_controller_strategy(self, name, controller_strategy):
        if name in self.controllers:
            raise ValueError(f"El controlador '{name}' ya está registrado.")
        self.controllers[name] = controller_strategy

    def get_repo(self, name):
        if name not in self.repositories:
            raise KeyError(f"El repositorio '{name}' no está registrado.")
        # Crear repositorio a través de la estrategia
        repository_strategy = self.repositories[name]
        return repository_strategy.create_repository(self.sql_operations)

    def get_controller(self, name):
        if name not in self.controllers:
            raise KeyError(f"El controlador '{name}' no está registrado.")
        # Crear controlador a través de la estrategia
        controller_strategy = self.controllers[name]
        return controller_strategy.create_controller(self.db_manager)
