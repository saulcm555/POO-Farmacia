import customtkinter as ctk
from models.empleado import Empleado

class EmpleadosView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title_label = ctk.CTkLabel(self, text="Gestión de Empleados", font=("Roboto", 24))
        self.title_label.pack(pady=20)

        # Frame para la lista de empleados
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.empleados_tree = ctk.CTkTreeview(self.list_frame, columns=("ID", "Nombre", "Teléfono", "Email", "Cargo", "Salario"))
        self.empleados_tree.heading("ID", text="ID")
        self.empleados_tree.heading("Nombre", text="Nombre")
        self.empleados_tree.heading("Teléfono", text="Teléfono")
        self.empleados_tree.heading("Email", text="Email")
        self.empleados_tree.heading("Cargo", text="Cargo")
        self.empleados_tree.heading("Salario", text="Salario")
        self.empleados_tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Frame para botones de acción
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(pady=10, padx=10, fill="x")

        self.add_button = ctk.CTkButton(self.action_frame, text="Agregar Empleado", command=self.show_add_employee)
        self.add_button.pack(side="left", padx=5)

        self.edit_button = ctk.CTkButton(self.action_frame, text="Editar Empleado", command=self.show_edit_employee)
        self.edit_button.pack(side="left", padx=5)

        self.delete_button = ctk.CTkButton(self.action_frame, text="Eliminar Empleado", command=self.delete_employee)
        self.delete_button.pack(side="left", padx=5)

        self.refresh_button = ctk.CTkButton(self.action_frame, text="Actualizar Lista", command=self.refresh_employees)
        self.refresh_button.pack(side="right", padx=5)

        self.refresh_employees()

    def refresh_employees(self):
        self.empleados_tree.delete(*self.empleados_tree.get_children())
        empleados = self.controller.obtener_todos_empleados()
        for empleado in empleados:
            self.empleados_tree.insert("", "end", values=(empleado.id_persona, empleado.nombre, empleado.telefono, empleado.email, empleado.cargo, empleado.salario))

    def show_add_employee(self):
        add_window = ctk.CTkToplevel(self)
        add_window.title("Agregar Empleado")
        add_window.geometry("400x400")
        add_window.grab_set()  # Make the window modal

        entries = {}
        for field in ["Nombre", "Teléfono", "Email", "Dirección", "Cargo", "Salario"]:
            ctk.CTkLabel(add_window, text=f"{field}:").pack(pady=5)
            entries[field.lower()] = ctk.CTkEntry(add_window)
            entries[field.lower()].pack(pady=5)

        def add_employee():
            try:
                nuevo_empleado = Empleado(
                    id_persona=None,  # The controller should handle ID generation
                    nombre=entries["nombre"].get(),
                    telefono=entries["teléfono"].get(),
                    email=entries["email"].get(),
                    direccion=entries["dirección"].get(),
                    cargo=entries["cargo"].get(),
                    salario=float(entries["salario"].get())
                )
                self.controller.agregar_empleado(nuevo_empleado)
                self.refresh_employees()
                add_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(add_window, text="Guardar", command=add_employee).pack(pady=20)

    def show_edit_employee(self):
        selected_item = self.empleados_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un empleado para editar.")
            return

        empleado_id = self.empleados_tree.item(selected_item)['values'][0]
        empleado = self.controller.obtener_empleado(empleado_id)

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Empleado")
        edit_window.geometry("400x400")
        edit_window.grab_set()  # Make the window modal

        entries = {}
        for field, value in [("Nombre", empleado.nombre), ("Teléfono", empleado.telefono), 
                             ("Email", empleado.email), ("Dirección", empleado.direccion),
                             ("Cargo", empleado.cargo), ("Salario", empleado.salario)]:
            ctk.CTkLabel(edit_window, text=f"{field}:").pack(pady=5)
            entries[field.lower()] = ctk.CTkEntry(edit_window)
            entries[field.lower()].insert(0, str(value))
            entries[field.lower()].pack(pady=5)

        def update_employee():
            try:
                empleado.nombre = entries["nombre"].get()
                empleado.telefono = entries["teléfono"].get()
                empleado.email = entries["email"].get()
                empleado.direccion = entries["dirección"].get()
                empleado.cargo = entries["cargo"].get()
                empleado.salario = float(entries["salario"].get())
                self.controller.actualizar_empleado(empleado)
                self.refresh_employees()
                edit_window.destroy()
            except ValueError as e:
                ctk.CTkMessagebox(title="Error", message=str(e))

        ctk.CTkButton(edit_window, text="Actualizar", command=update_employee).pack(pady=20)

    def delete_employee(self):
        selected_item = self.empleados_tree.selection()
        if not selected_item:
            ctk.CTkMessagebox(title="Error", message="Por favor, seleccione un empleado para eliminar.")
            return

        empleado_id = self.empleados_tree.item(selected_item)['values'][0]
        confirm = ctk.CTkMessagebox(title="Confirmar eliminación", 
                                    message="¿Está seguro de que desea eliminar este empleado?", 
                                    icon="warning", 
                                    option_1="Sí", 
                                    option_2="No")
        if confirm.get() == "Sí":
            try:
                self.controller.eliminar_empleado(empleado_id)
                self.refresh_employees()
            except Exception as e:
                ctk.CTkMessagebox(title="Error", message=f"No se pudo eliminar el empleado: {str(e)}")