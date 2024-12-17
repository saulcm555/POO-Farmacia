import customtkinter as ctk
from models.cliente import Cliente

class ClientesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title_label = ctk.CTkLabel(self, text="Gestión de Clientes", font=("Roboto", 24))
        self.title_label.pack(pady=20)

        
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.clientes_tree = ctk.CTkTreeview(self.list_frame, columns=("ID", "Nombre", "Teléfono", "Email", "Puntos"))
        self.clientes_tree.heading("ID", text="ID")
        self.clientes_tree.heading("Nombre", text="Nombre")
        self.clientes_tree.heading("Teléfono", text="Teléfono")
        self.clientes_tree.heading("Email", text="Email")
        self.clientes_tree.heading("Puntos", text="Puntos de Fidelidad")
        self.clientes_tree.pack(pady=10, padx=10, fill="both", expand=True)

        
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(pady=10, padx=10, fill="x")

        self.add_button = ctk.CTkButton(self.action_frame, text="Agregar Cliente", command=self.show_add_client)
        self.add_button.pack(side="left", padx=5)

        self.edit_button = ctk.CTkButton(self.action_frame, text="Editar Cliente", command=self.show_edit_client)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(self.action_frame, text="Eliminar Cliente", command=self.delete_client)
        self.delete_button.pack(side="left", padx=5)

        self.refresh_button = ctk.CTkButton(self.action_frame, text="Actualizar Lista", command=self.refresh_clients)
        self.refresh_button.pack(side="right", padx=5)

        self.refresh_clients()

    def refresh_clients(self):
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        clientes = self.controller.obtener_todos_clientes()
        for cliente in clientes:
            self.clientes_tree.insert("", "end", values=(cliente.id_persona, cliente.nombre, cliente.telefono, cliente.email, cliente.puntos_fidelidad))

    def show_add_client(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Agregar Cliente")
        add_window.geometry("400x300")
        add_window.grab_set()  

        entries = {}
        for field in ["Nombre", "Teléfono", "Email", "Dirección"]:
            ctk.CTkLabel(add_window, text=f"{field}:").pack(pady=5)
            entries[field.lower()] = ctk.CTkEntry(add_window)
            entries[field.lower()].pack(pady=5)

        def add_client():
            try:
                nuevo_cliente = Cliente(
                    id_persona=None,  
                    nombre=entries["nombre"].get(),
                    telefono=entries["teléfono"].get(),
                    email=entries["email"].get(),
                    direccion=entries["dirección"].get()
                )
                self.controller.agregar_cliente(nuevo_cliente)
                self.refresh_clients()
                add_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(add_window, text="Guardar", command=add_client).pack(pady=20)

    def show_edit_client(self):
        selected_item = self.clientes_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un cliente para editar.")
            return

        cliente_id = self.clientes_tree.item(selected_item)['values'][0]
        cliente = self.controller.obtener_cliente(cliente_id)

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Cliente")
        edit_window.geometry("400x300")
        edit_window.grab_set()  

        entries = {}
        for field, value in [("Nombre", cliente.nombre), ("Teléfono", cliente.telefono), 
                             ("Email", cliente.email), ("Dirección", cliente.direccion)]:
            ctk.CTkLabel(edit_window, text=f"{field}:").pack(pady=5)
            entries[field.lower()] = ctk.CTkEntry(edit_window)
            entries[field.lower()].insert(0, value)
            entries[field.lower()].pack(pady=5)

        def update_client():
            try:
                cliente.nombre = entries["nombre"].get()
                cliente.telefono = entries["teléfono"].get()
                cliente.email = entries["email"].get()
                cliente.direccion = entries["dirección"].get()
                self.controller.actualizar_cliente(cliente)
                self.refresh_clients()
                edit_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(edit_window, text="Actualizar", command=update_client).pack(pady=20)

    def delete_client(self):
        selected_item = self.clientes_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un cliente para eliminar.")
            return

        cliente_id = self.clientes_tree.item(selected_item)['values'][0]
        confirm = ctk.CTkMessagebox(title="Confirmar eliminación", 
                                    message="¿Está seguro de que desea eliminar este cliente?", 
                                    icon="warning", 
                                    option_1="Sí", 
                                    option_2="No")
        if confirm.get() == "Sí":
            try:
                self.controller.eliminar_cliente(cliente_id)
                self.refresh_clients()
            except Exception as e:
                ctk.CTkMessagebox(title="Error", message=f"No se pudo eliminar el cliente: {str(e)}")