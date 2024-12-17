from abc import ABC, abstractmethod

from database.repositories import (
    UserRepository,
    MedicineRepository,
    SalesRepository,
)

class RepositoryStrategy(ABC):
    @abstractmethod
    def create_repository(self, sql_operations):
        pass


class UserRepositoryStrategy(RepositoryStrategy):
    def create_repository(self, sql_operations):
        return UserRepository(sql_operations)


class MedicineRepositoryStrategy(RepositoryStrategy):
    def create_repository(self, sql_operations):
        return MedicineRepository(sql_operations)




class SalesRepositoryStrategy(RepositoryStrategy):
    def create_repository(self, sql_operations):
        return SalesRepository(sql_operations)