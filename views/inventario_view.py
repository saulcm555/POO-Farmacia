import customtkinter as ctk
from tkinter import ttk 
from models.medicamento import MedicamentoGenerico, MedicamentoMarca


class InventarioView(ctk.CTkFrame):
    def __init__(self, master, content_frame, controller, user_login):
        super().__init__(content_frame)
        self.inventory_controller = controller
        self.master = master
        self.user_login = user_login
        self.notifications = master.di.get_controller("notifications")

        self._crear_interfaz()
        self.actualizar_inventario()

    def _crear_interfaz(self):
        self.title_label = ctk.CTkLabel(
            self, text="Gestion de Inventario", font=("Roboto", 24)
        )
        self.title_label.pack(pady=20)

        self._crear_frame_busqueda()
        self._crear_lista_medicamentos()
        self._crear_frame_acciones()

    def _crear_frame_busqueda(self):
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10, padx=10, fill="x")

        self.search_entry = ctk.CTkEntry(
            self.search_frame, placeholder_text="Buscar medicamento"
        )
        self.search_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.search_button = ctk.CTkButton(
            self.search_frame, text="Buscar", command=self.buscar_medicamento
        )
        self.search_button.pack(side="right")

    def _crear_lista_medicamentos(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.medicamentos_tree = ttk.Treeview(
            self.list_frame,
            columns=(
                "Codigo",
                "Nombre",
                "Proveedor",
                "Tipo",
                "Precio",
                "Fecha_caducidad",
                "Stock",
            ),
            show="headings",
        )
        for column in self.medicamentos_tree["columns"]:
            self.medicamentos_tree.heading(column, text=column)

        self.medicamentos_tree.pack(pady=10, padx=10, fill="both", expand=True)

    def _crear_frame_acciones(self):
        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.pack(pady=10, padx=10, fill="x")

        if self.user_login.get_current_user().obtener_tipo() == "Empleado":
            self._crear_boton("Agregar Medicamento", self.mostrar_agregar_medicamento)
            self._crear_boton("Editar Medicamento", self.mostrar_editar_medicamento)
            self._crear_boton("Eliminar Medicamento", self.eliminar_medicamento)

        self.actualizar_button = ctk.CTkButton(
            self.action_frame,
            text="Actualizar Inventario",
            command=self.actualizar_inventario,
        )
        self.actualizar_button.pack(side="right", padx=5)

    def _crear_boton(self, text, command):
        button = ctk.CTkButton(self.action_frame, text=text, command=command)
        button.pack(side="left", padx=5)

    def buscar_medicamento(self):
        criterio = self.search_entry.get().strip()
        resultados = self.inventory_controller.buscar_medicamento_similares(criterio)
        self.actualizar_tree(resultados)

    def actualizar_tree(self, medicamentos):
        self.medicamentos_tree.delete(*self.medicamentos_tree.get_children())
        for medicamento in medicamentos:
            tipo = (
                "Genérico" if isinstance(medicamento, MedicamentoGenerico) else "Marca"
            )
            self.medicamentos_tree.insert(
                "",
                "end",
                values=(
                    medicamento._codigo,
                    medicamento._nombre,
                    medicamento.proveedor,
                    tipo,
                    f"${medicamento._precio:.2f}",
                    medicamento.fecha_caducidad,
                    medicamento.stock,
                ),
            )

    def mostrar_agregar_medicamento(self):
        self._crear_ventana_medicamento("Agregar Medicamento", self.agregar_medicamento)

    def mostrar_editar_medicamento(self):
        selected_item = self.medicamentos_tree.selection()
        if not selected_item:
            self.notifications.show_error(
                "Error", "Seleccione un medicamento para editar."
            )
            return

        codigo = self.medicamentos_tree.item(selected_item)["values"][0]
        medicamento = self.inventory_controller.buscar_medicamento_por_codigo(codigo)

        self._crear_ventana_medicamento(
            "Editar Medicamento", self.actualizar_medicamento, medicamento
        )

    def _crear_ventana_medicamento(self, titulo, accion, medicamento=None):
        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("400x600")
        ventana.grab_set()

        entries = self._crear_formulario(ventana, medicamento)
        tipo_var = ctk.StringVar(
            value=(
                "Genérico"
                if medicamento and isinstance(medicamento, MedicamentoGenerico)
                else "Marca"
            )
        )
        ctk.CTkSwitch(
            ventana,
            text="Tipo",
            variable=tipo_var,
            onvalue="Marca",
            offvalue="Genérico",
        ).pack(pady=10)

        def manejar_accion():
            try:
                datos = self._obtener_datos_formulario(entries)
                es_generico = tipo_var.get() == "Genérico"
                medicamento_class = (
                    MedicamentoGenerico if es_generico else MedicamentoMarca
                )
                medicamento_obj = medicamento_class(**datos)
                accion(medicamento_obj)
                ventana.destroy()
                self.actualizar_inventario()
                self.notifications.show_info("Éxito", f"{titulo} exitoso.")
            except ValueError:
                self.notifications.show_error("Error", "Datos inválidos.")

        ctk.CTkButton(ventana, text=titulo.split()[0], command=manejar_accion).pack(
            pady=20
        )

    def _crear_formulario(self, ventana, medicamento=None):
        fields = ["Codigo", "Nombre", "Proveedor", "Precio", "Fecha_Caducidad", "Stock"]
        entries = {}

        for field in fields:
            ctk.CTkLabel(ventana, text=f"{field}:").pack(pady=5)
            entry = ctk.CTkEntry(ventana)

            if medicamento:
                if field.lower() == "codigo":
                    entry.insert(0, medicamento._codigo)  
                elif field.lower() == "nombre":
                    entry.insert(0, medicamento._nombre)
                elif field.lower() == "proveedor":
                    entry.insert(0, medicamento.proveedor)
                elif field.lower() == "precio":
                    entry.insert(0, medicamento._precio)
                elif field.lower() == "fecha_caducidad":
                    entry.insert(0, medicamento.fecha_caducidad)
                elif field.lower() == "stock":
                    entry.insert(0, medicamento.stock)

            entry.pack(pady=5)
            entries[field.lower()] = entry
        return entries


    def _obtener_datos_formulario(self, entries):
        return {
            key: (float(value.get()) if key == "precio" else value.get().strip())
            for key, value in entries.items()
        }

    def agregar_medicamento(self, medicamento):
        self.inventory_controller.agregar_medicamento(medicamento)

    def actualizar_medicamento(self, medicamento):
        
        self.inventory_controller.actualizar_medicamento(medicamento)

    def eliminar_medicamento(self):
        selected_item = self.medicamentos_tree.selection()
        if not selected_item:
            self.notifications.show_error(
                "Error", "Seleccione un medicamento para eliminar."
            )
            return

        codigo = self.medicamentos_tree.item(selected_item)["values"][0]
        if self.notifications.show_confirmation(
            "Eliminar Medicamento", "¿Está seguro?"
        ):
            self.inventory_controller.eliminar_medicamento(codigo)
            self.actualizar_inventario()
            self.notifications.show_info("Éxito", "Medicamento eliminado.")

    def actualizar_inventario(self):
        medicamentos = self.inventory_controller.obtener_todos_medicamentos()
        self.actualizar_tree(medicamentos)
