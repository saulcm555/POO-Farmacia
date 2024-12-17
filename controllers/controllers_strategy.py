from abc import ABC, abstractmethod


from controllers import (
    AuthController,
    InventoryController,
    VentasController,
    UsersController,
)

from services.user_login import UserLogin
from utils.notifications import Notifications





# Estrategia para crear controladores
class ControllerStrategy(ABC):
    @abstractmethod
    def create_controller(self, db_manager):
        pass


class AuthControllerStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return AuthController(db_manager)


class InventoryControllerStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return InventoryController(db_manager)


class NotificationsStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return Notifications()


class VentasControllerStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return VentasController(db_manager)


class ClientesControllerStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return UsersController(db_manager)


class UserLoginStrategy(ControllerStrategy):
    def create_controller(self, db_manager):
        return UserLogin(db_manager)
