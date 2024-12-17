from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, username:str) :
        pass

    @abstractmethod
    def create_user(self, username:str, password:str, role:str, telefono:str, email:str, direccion:str) :
        pass