import customtkinter as ctk
from models.proveedor import Proveedor

class ProveedoresView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Gestión de Proveedores", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")

        # Frame para la lista de proveedores
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.proveedores_tree = ctk.CTkTreeview(self.list_frame, columns=("ID", "Nombre", "Teléfono", "Email", "Dirección"))
        self.proveedores_tree.heading("ID", text="ID")
        self.proveedores_tree.heading("Nombre", text="Nombre")
        self.proveedores_tree.heading("Teléfono", text="Teléfono")
        self.proveedores_tree.heading("Email", text="Email")
        self.proveedores_tree.heading("Dirección", text="Dirección")
        self.proveedores_tree.grid(row=0, column=0, sticky="nsew")

        # Frame para botones de acción
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.add_button = ctk.CTkButton(self.action_frame, text="Agregar Proveedor", command=self.show_add_provider)
        self.add_button.grid(row=0, column=0, padx=(0, 10))

        self.edit_button = ctk.CTkButton(self.action_frame, text="Editar Proveedor", command=self.show_edit_provider)
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ctk.CTkButton(self.action_frame, text="Eliminar Proveedor", command=self.delete_provider)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.refresh_button = ctk.CTkButton(self.action_frame, text="Actualizar Lista", command=self.refresh_providers)
        self.refresh_button.grid(row=0, column=3, padx=(10, 0))

        self.refresh_providers()

    def refresh_providers(self):
        self.proveedores_tree.delete(*self.proveedores_tree.get_children())
        proveedores = self.controller.obtener_todos_proveedores()
        for proveedor in proveedores:
            self.proveedores_tree.insert("", "end", values=(proveedor.id_proveedor, proveedor.nombre, proveedor.telefono, proveedor.email, proveedor.direccion))

    def show_add_provider(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Agregar Proveedor")
        add_window.geometry("400x350")
        add_window.grab_set()

        ctk.CTkLabel(add_window, text="Agregar Nuevo Proveedor", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        fields = ["Nombre", "Teléfono", "Email", "Dirección"]
        entries = {}

        for field in fields:
            frame = ctk.CTkFrame(add_window)
            frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(frame, text=f"{field}:").pack(side="left")
            entries[field.lower()] = ctk.CTkEntry(frame)
            entries[field.lower()].pack(side="right", expand=True, fill="x", padx=(10, 0))

        def add_provider():
            try:
                nuevo_proveedor = Proveedor(
                    id_proveedor=None,  # El controlador debería manejar la generación de ID
                    nombre=entries["nombre"].get(),
                    telefono=entries["teléfono"].get(),
                    email=entries["email"].get(),
                    direccion=entries["dirección"].get()
                )
                self.controller.agregar_proveedor(nuevo_proveedor)
                self.refresh_providers()
                add_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(add_window, text="Guardar", command=add_provider).pack(pady=20)

    def show_edit_provider(self):
        selected_item = self.proveedores_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un proveedor para editar.")
            return

        proveedor_id = self.proveedores_tree.item(selected_item)['values'][0]
        proveedor = self.controller.obtener_proveedor(proveedor_id)

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Proveedor")
        edit_window.geometry("400x350")
        edit_window.grab_set()

        ctk.CTkLabel(edit_window, text="Editar Proveedor", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))

        fields = ["Nombre", "Teléfono", "Email", "Dirección"]
        entries = {}

        for field in fields:
            frame = ctk.CTkFrame(edit_window)
            frame.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(frame, text=f"{field}:").pack(side="left")
            entries[field.lower()] = ctk.CTkEntry(frame)
            entries[field.lower()].pack(side="right", expand=True, fill="x", padx=(10, 0))
            entries[field.lower()].insert(0, getattr(proveedor, field.lower()))

        def update_provider():
            try:
                proveedor.nombre = entries["nombre"].get()
                proveedor.telefono = entries["teléfono"].get()
                proveedor.email = entries["email"].get()
                proveedor.direccion = entries["dirección"].get()
                self.controller.actualizar_proveedor(proveedor)
                self.refresh_providers()
                edit_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(edit_window, text="Actualizar", command=update_provider).pack(pady=20)

    def delete_provider(self):
        selected_item = self.proveedores_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un proveedor para eliminar.")
            return

        proveedor_id = self.proveedores_tree.item(selected_item)['values'][0]
        confirm = ctk.CTkMessagebox(title="Confirmar eliminación", 
                                    message="¿Está seguro de que desea eliminar este proveedor?", 
                                    icon="warning", 
                                    option_1="Sí", 
                                    option_2="No")
        if confirm.get() == "Sí":
            try:
                self.controller.eliminar_proveedor(proveedor_id)
                self.refresh_providers()
            except Exception as e:
                ctk.CTkMessagebox(title="Error", message=f"No se pudo eliminar el proveedor: {str(e)}")