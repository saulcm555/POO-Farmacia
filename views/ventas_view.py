import customtkinter as ctk
from tkinter.ttk import Treeview, Style, Combobox
from models.medicamento import MedicamentoMarca

class VentasView(ctk.CTkFrame):
    def __init__(self, master, content_frame, controller, clientes_controller, inventario_controller):
        super().__init__(content_frame)
        self.master = master
        self.notifications = master.di.get_controller("notifications")
        self.controller = controller
        self.clientes_controller = clientes_controller
        self.inventario_controller = inventario_controller

        self.clientes = self.cargar_clientes()
        self.empleados = self.cargar_empleados()

        # Configuración de la grilla
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título
        self.title_label = ctk.CTkLabel(self, text="Registro de Ventas", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")

        # Información de cliente y empleado
        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.info_frame.grid_columnconfigure(1, weight=1)

        self._crear_dropdown(self.info_frame, "Cliente:", self.cargar_clientes_dropdown, 0)
        self._crear_dropdown(self.info_frame, "Empleado:", self.cargar_empleados_dropdown, 1)

        # Tabla de medicamentos
        self._crear_tabla_medicamentos()

        # Botones de acción
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
        self._crear_botones_accion()

    def _crear_dropdown(self, parent, label_text, cargar_func, row):
        label = ctk.CTkLabel(parent, text=label_text)
        label.grid(row=row, column=0, padx=(0, 10), pady=10, sticky="w")
        
        dropdown = Combobox(parent, state="readonly", width=40)
        dropdown["values"] = cargar_func()
        dropdown.grid(row=row, column=1, padx=10, pady=10, sticky="ew")

        setattr(self, f"{label_text.lower().strip(':')}_dropdown", dropdown)

    def _crear_tabla_medicamentos(self):
        self.medicamentos_frame = ctk.CTkFrame(self)
        self.medicamentos_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.medicamentos_frame.grid_rowconfigure(0, weight=1)
        self.medicamentos_frame.grid_columnconfigure(0, weight=1)

        self.medicamentos_tree = Treeview(self.medicamentos_frame, columns=("Código", "Nombre", "Cantidad", "Precio", "Total"), show="headings")
        for col in [("Código", 100), ("Nombre", 200), ("Cantidad", 100), ("Precio", 100), ("Total", 100)]:
            self.medicamentos_tree.heading(col[0], text=col[0])
            self.medicamentos_tree.column(col[0], width=col[1], anchor="center" if col[0] != "Nombre" else "w")

        self.medicamentos_tree.grid(row=0, column=0, sticky="nsew")
        style = Style()
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

    def _crear_botones_accion(self):
        self.agregar_medicamento_button = ctk.CTkButton(self.button_frame, text="Agregar Medicamento", command=self.agregar_medicamento_venta)
        self.agregar_medicamento_button.pack(side="left", padx=(0, 10))

        self.eliminar_medicamento_button = ctk.CTkButton(self.button_frame, text="Eliminar Medicamento", command=self.eliminar_medicamento_venta)
        self.eliminar_medicamento_button.pack(side="left", padx=10)

        self.realizar_venta_button = ctk.CTkButton(self.button_frame, text="Realizar Venta", command=self.realizar_venta)
        self.realizar_venta_button.pack(side="right", padx=(10, 0))

    def cargar_clientes(self):
        return self.clientes_controller.listar_clientes()

    def cargar_empleados(self):
        return self.clientes_controller.listar_empleados()

    def cargar_clientes_dropdown(self):
        return [f"|{c.id_persona}| - {c.nombre}" for c in self.clientes]

    def cargar_empleados_dropdown(self):
        return [f"|{e.id_persona}| - {e.nombre}" for e in self.empleados]

    def agregar_medicamento_venta(self):
        def add_medicamento():
            try:
                codigo = codigo_entry.get().strip()
                cantidad = int(cantidad_entry.get().strip())
                if cantidad <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0")
                
                medicamento = self.inventario_controller.buscar_medicamento_por_codigo(codigo)
                if not medicamento:
                    raise ValueError("No se encontró el medicamento")

                if cantidad > medicamento.stock:
                    raise ValueError("No hay suficiente stock disponible")

                total = medicamento._precio * cantidad
                self.medicamentos_tree.insert("", "end", values=(medicamento._codigo, medicamento._nombre, cantidad, f"${medicamento._precio:.2f}", f"${total:.2f}"))
                add_window.destroy()
            except ValueError as e:
                self.notifications.show_error("Error", str(e))

        add_window = ctk.CTkToplevel(self)
        add_window.title("Agregar Medicamento")
        add_window.geometry("300x300")
        add_window.grab_set()

        ctk.CTkLabel(add_window, text="Código Medicamento:").pack(pady=(20, 5))
        codigo_entry = ctk.CTkEntry(add_window)
        codigo_entry.pack(pady=5)

        ctk.CTkLabel(add_window, text="Cantidad:").pack(pady=5)
        cantidad_entry = ctk.CTkEntry(add_window)
        cantidad_entry.pack(pady=5)

        ctk.CTkButton(add_window, text="Agregar", command=add_medicamento).pack(pady=20)

    def eliminar_medicamento_venta(self):
        selected_item = self.medicamentos_tree.selection()
        if selected_item:
            self.medicamentos_tree.delete(selected_item)
        else:
            self.notifications.show_error("Error", "Por favor, seleccione un medicamento para eliminar")

    def realizar_venta(self):
        try:
            cliente_id = self.obtener_id_seleccionado(self.cliente_dropdown.get(), self.clientes)
            empleado_id = self.obtener_id_seleccionado(self.empleado_dropdown.get(), self.empleados)

            medicamentos = [
                (self.inventario_controller.buscar_medicamento_por_codigo(values[0]), int(values[2]))
                for values in (self.medicamentos_tree.item(item)["values"] for item in self.medicamentos_tree.get_children())
            ]

            if not medicamentos:
                raise ValueError("No hay medicamentos para la venta")

            total = sum(m[1] * m[0]._precio for m in medicamentos)
            self.controller.realizar_venta(cliente_id, empleado_id, medicamentos)
            self.notifications.show_info("Venta realizada", f"Venta realizada con éxito. Total: ${total:.2f}")
            self.limpiar_formulario()
        except ValueError as e:
            self.notifications.show_error("Error", str(e))

    def limpiar_formulario(self):
        self.cliente_dropdown.set("")
        self.empleado_dropdown.set("")
        for item in self.medicamentos_tree.get_children():
            self.medicamentos_tree.delete(item)

    def obtener_id_seleccionado(self, seleccion, lista):
        if not seleccion:
            raise ValueError("Debe seleccionar un cliente y un empleado")
        return next((obj.id_persona for obj in lista if f"|{obj.id_persona}|" in seleccion), None)
