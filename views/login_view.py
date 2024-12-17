import customtkinter as ctk


class LoginView(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, controller, user_login, *args, **kwargs):
        super().__init__(master)

        self.master.set_geometry(400, 500)
        self.user_login = user_login

        self.auth_controller = controller
        self.notifications = self.master.di.get_controller("notifications")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.login_frame.grid_rowconfigure(5, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.login_frame, text="Farmacia Login", font=("Roboto", 24)
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.username_entry = ctk.CTkEntry(
            self.login_frame, placeholder_text="Usuario", width=200
        )
        self.username_entry.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.password_frame = ctk.CTkFrame(self.login_frame)
        self.password_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        self.password_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            self.password_frame, placeholder_text="Contraseña", show="*", width=200
        )
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.show_password = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=30,
            command=self.toggle_password_visibility,
        )
        self.show_password.grid(row=0, column=1, padx=(5, 0))

        self.remember_var = ctk.BooleanVar()
        self.remember_checkbox = ctk.CTkCheckBox(
            self.login_frame, text="Recordarme", variable=self.remember_var
        )
        self.remember_checkbox.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="w")

        self.login_button = ctk.CTkButton(
            self.login_frame, text="Iniciar sesión", command=self.login, width=200
        )
        self.login_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.register_button = ctk.CTkButton(
            self.login_frame,
            text="¿No tienes cuenta? Regístrate",
            command=self.show_register_view,
            width=200,
        )
        self.register_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

    def show_register_view(self):
        self.master.show_register_view()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.notifications.show_error(
                "Error de inicio de sesión", "Por favor, ingrese usuario y contraseña"
            )
            return

        user = self.user_login.login(username, password)
        if user:

            self.master.show_main_view(user)
        else:
            self.notifications.show_error(
                "Error de inicio de sesión", "Usuario o contraseña incorrectos"
            )
            return

    def toggle_password_visibility(self):
        current_show_value = self.password_entry.cget("show")
        new_show_value = "" if current_show_value == "*" else "*"
        self.password_entry.configure(show=new_show_value)

    def reset_form(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.remember_var.set(False)
