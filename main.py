import customtkinter as ctk
from views.cuentas import LoginView, RegisterView
from views.main_view import MainView
from dependency_injector import DependencyInjector
from utils.view_manager import ViewManager


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Ventas")
        self.di = DependencyInjector()
        self.view_manager = ViewManager(self)
        self.show_login_view()

    def show_login_view(self):
        self.view_manager.show_view(
            LoginView,
            self.di.get_controller("auth_controller"),
            self.di.get_controller("user_login"),
        )

    def show_register_view(self):
        self.view_manager.show_view(
            RegisterView, self.di.get_controller("auth_controller")
        )

    def show_main_view(self, user):
        self.view_manager.show_view(
            MainView,
            user,
            self.di.get_controller("auth_controller"),
            self.di.get_controller("inventario_controller"),
            self.di.get_controller("ventas_controller"),
            self.di.get_controller("clientes_controller"),
            self.di.get_controller("user_login"),
        )

    def set_geometry(self, width, height):
        self.geometry(f"{width}x{height}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
