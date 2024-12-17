import customtkinter as ctk
from tkinter import messagebox

class RegisterView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.master.set_geometry(400, 700)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.register_frame.grid_rowconfigure(10, weight=1)
        self.register_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.register_frame, text="Registro de Usuario", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        fields = [
            ("Usuario", "username"),
            ("Correo electrónico", "email"),
            ("Contraseña", "password"),
            ("Confirmar contraseña", "confirm_password")
        ]

        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ctk.CTkLabel(self.register_frame, text=label).grid(row=i*2+1, column=0, padx=20, pady=(10, 0), sticky="w")
            entry = ctk.CTkEntry(self.register_frame, width=200, show="*" if "password" in key else "")
            entry.grid(row=i*2+2, column=0, padx=20, pady=(0, 10), sticky="ew")
            self.entries[key] = entry

        self.show_password_var = ctk.BooleanVar()
        self.show_password_checkbox = ctk.CTkCheckBox(self.register_frame, text="Mostrar contraseña", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=9, column=0, padx=20, pady=(0, 10), sticky="w")

        # Aquí estaba el problema con `role_var`
        self.role_var = ctk.StringVar(value="cliente")  # Corregido
        self.role_label = ctk.CTkLabel(self.register_frame, text="Rol:")
        self.role_label.grid(row=10, column=0, padx=20, pady=(10, 0), sticky="w")
        self.role_radio_frame = ctk.CTkFrame(self.register_frame)
        self.role_radio_frame.grid(row=11, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.empleado_radio = ctk.CTkRadioButton(self.role_radio_frame, text="cliente", variable=self.role_var, value="cliente")
        self.empleado_radio.pack(side="left", padx=(0, 10))
        self.admin_radio = ctk.CTkRadioButton(self.role_radio_frame, text="admin", variable=self.role_var, value="admin")
        self.admin_radio.pack(side="left")

        self.register_button = ctk.CTkButton(self.register_frame, text="Registrarse", command=self.register, width=200)
        self.register_button.grid(row=12, column=0, padx=20, pady=10, sticky="ew")

        self.error_label = ctk.CTkLabel(self.register_frame, text="", text_color="red")
        self.error_label.grid(row=13, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.back_button = ctk.CTkButton(self.register_frame, text="Volver al inicio de sesión", command=self.back_to_login, width=200)
        self.back_button.grid(row=14, column=0, padx=20, pady=(0, 20), sticky="ew")

    def toggle_password_visibility(self):
        new_show_value = "" if self.show_password_var.get() else "*"
        self.entries["password"].configure(show=new_show_value)
        self.entries["confirm_password"].configure(show=new_show_value)

    def register(self):
        username = self.entries["username"].get()
        email = self.entries["email"].get()
        password = self.entries["password"].get()
        confirm_password = self.entries["confirm_password"].get()
        role = self.role_var.get().lower()  # Convertir a minúsculas

        if not username or not email or not password or not confirm_password:
            self.error_label.configure(text="Por favor, complete todos los campos")
            return

        if password != confirm_password:
            self.error_label.configure(text="Las contraseñas no coinciden")
            return

        try:
            # Ahora se utiliza el valor normalizado del rol
            user = self.controller.register(username=username, password=password, role=role, email=email)
            if user:
                messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
                self.reset_form()
                self.master.show_login_view()
            else:
                self.error_label.configure(text="Error al registrar el usuario")
        except Exception as e:
            self.error_label.configure(text=f"Error de registro: {str(e)}")


    def back_to_login(self):
        self.reset_form()
        self.master.show_login_view()

    def reset_form(self):
        for entry in self.entries.values():
            entry.delete(0, 'end')
        self.role_var.set("empleado")
        self.error_label.configure(text="")
        self.show_password_var.set(False)
        self.toggle_password_visibility()
