import customtkinter as ctk
from utils.utils_ctk import UtilsCTK
from views.inventario_view import InventarioView
from views.ventas_view import VentasView

class MainView(ctk.CTkFrame):
    def __init__(self, master, user, auth_controller, inventario_controller, ventas_controller, clientes_controller, user_login):
        super().__init__(master)
        self.master.set_geometry(1500, 600)
        self.user = user
        self.auth_controller = auth_controller
        self.inventario_controller = inventario_controller
        self.ventas_controller = ventas_controller
        self.clientes_controller = clientes_controller
        self.user_login = user_login

        
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=0)  
        self.grid_columnconfigure(1, weight=1)  

        
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")  
        self.sidebar.grid_rowconfigure(7, weight=1)  

        
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="Farmacia App", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.welcome_label = ctk.CTkLabel(
            self.sidebar, text=f"Bienvenido,\n{user.nombre}", font=ctk.CTkFont(size=14)
        )
        self.welcome_label.grid(row=1, column=0, padx=20, pady=(10, 20))

        
        self.inventario_button = ctk.CTkButton(
            self.sidebar, text="Inventario", command=self.show_inventario
        )
        self.inventario_button.grid(row=2, column=0, padx=20, pady=10)

        self.ventas_button = ctk.CTkButton(
            self.sidebar, text="Ventas", command=self.show_ventas
        )
        self.ventas_button.grid(row=3, column=0, padx=20, pady=10)

        self.logout_button = ctk.CTkButton(
            self.sidebar, text="Cerrar Sesión", command=self.logout
        )
        self.logout_button.grid(row=8, column=0, padx=20, pady=(10, 20))

        
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        
        self.show_inventario()

    def show_inventario(self):
        UtilsCTK.clean_window(self.content_frame)
        inventario_view = InventarioView(self.master,self.content_frame, self.inventario_controller, self.user_login)
        inventario_view.pack(fill="both", expand=True)  

    def show_ventas(self):
        UtilsCTK.clean_window(self.content_frame)
        ventas_view = VentasView(self.master, self.content_frame, self.ventas_controller, self.clientes_controller, self.inventario_controller)
        ventas_view.pack(fill="both", expand=True)

    def logout(self):
        self.auth_controller.logout()  
        self.master.di.get_controller("notifications").show_info(
            "Sesión cerrada", "Sesión cerrada exitosamente."
        )
        self.master.show_login_view()  
