from abc import ABC, abstractmethod  # Importa ABC y abstractmethod para clases abstractas

from database.repositories import (  # Importa las clases de repositorios necesarias
    UserRepository,
    MedicineRepository,
    SalesRepository,
)

class RepositoryStrategy(ABC):  # Clase abstracta para definir una estrategia de repositorio
    @abstractmethod
    def create_repository(self, sql_operations):  # Método abstracto para crear un repositorio
        pass


class UserRepositoryStrategy(RepositoryStrategy):  # Estrategia para el repositorio de usuarios
    def create_repository(self, sql_operations):
        return UserRepository(sql_operations)  # Retorna una instancia de UserRepository


class MedicineRepositoryStrategy(RepositoryStrategy):  # Estrategia para el repositorio de medicamentos
    def create_repository(self, sql_operations):
        return MedicineRepository(sql_operations)  # Retorna una instancia de MedicineRepository


class SalesRepositoryStrategy(RepositoryStrategy):  # Estrategia para el repositorio de ventas
    def create_repository(self, sql_operations):
        return SalesRepository(sql_operations)  # Retorna una instancia de SalesRepository
