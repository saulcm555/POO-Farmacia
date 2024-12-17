import customtkinter as ctk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self, text="Generación de Reportes", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=20, sticky="ew")

        # Frame para selección de reportes
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.selection_frame.grid_columnconfigure(1, weight=1)

        self.report_type_label = ctk.CTkLabel(self.selection_frame, text="Tipo de Reporte:")
        self.report_type_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

        self.report_type = ctk.CTkComboBox(self.selection_frame, values=["Ventas por período", "Inventario actual", "Medicamentos más vendidos"])
        self.report_type.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.generate_button = ctk.CTkButton(self.selection_frame, text="Generar Reporte", command=self.generate_report)
        self.generate_button.grid(row=0, column=2, padx=(10, 0), pady=10, sticky="e")

        # Frame para mostrar el reporte
        self.report_frame = ctk.CTkFrame(self)
        self.report_frame.grid(row=2, column=0, pady=10, padx=20, sticky="nsew")
        self.report_frame.grid_rowconfigure(0, weight=1)
        self.report_frame.grid_columnconfigure(0, weight=1)

    def generate_report(self):
        report_type = self.report_type.get()
        
        # Limpiar el frame de reporte anterior
        for widget in self.report_frame.winfo_children():
            widget.destroy()

        try:
            if report_type == "Ventas por período":
                self.generate_sales_report()
            elif report_type == "Inventario actual":
                self.generate_inventory_report()
            elif report_type == "Medicamentos más vendidos":
                self.generate_top_selling_report()
            else:
                raise ValueError("Tipo de reporte no válido")
        except Exception as e:
            self.show_error(f"Error al generar el reporte: {str(e)}")

    def generate_sales_report(self):
        try:
            # Obtener datos de ventas
            ventas = self.controller.obtener_ventas(datetime.now() - timedelta(days=30), datetime.now())
            
            if not ventas:
                self.show_message("No hay datos de ventas para el período seleccionado.")
                return

            # Crear gráfico
            fig, ax = plt.subplots(figsize=(10, 5))
            dates = [venta.fecha for venta in ventas]
            amounts = [venta.total for venta in ventas]
            ax.plot(dates, amounts)
            ax.set_title("Ventas de los últimos 30 días")
            ax.set_xlabel("Fecha")
            ax.set_ylabel("Monto de venta")
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Mostrar gráfico en la interfaz
            canvas = FigureCanvasTkAgg(fig, master=self.report_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            self.show_error(f"Error al generar el reporte de ventas: {str(e)}")

    def generate_inventory_report(self):
        try:
            # Obtener datos de inventario
            inventario = self.controller.obtener_inventario()

            if not inventario:
                self.show_message("No hay datos de inventario disponibles.")
                return

            # Crear tabla de inventario
            tree = ctk.CTkTreeview(self.report_frame, columns=("Código", "Nombre", "Stock", "Precio"))
            tree.heading("Código", text="Código")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Stock", text="Stock")
            tree.heading("Precio", text="Precio")
            tree.grid(row=0, column=0, sticky="nsew")

            for medicamento in inventario:
                tree.insert("", "end", values=(medicamento.codigo, medicamento.nombre, medicamento.stock, f"${medicamento.precio:.2f}"))
        except Exception as e:
            self.show_error(f"Error al generar el reporte de inventario: {str(e)}")

    def generate_top_selling_report(self):
        try:
            # Obtener datos de medicamentos más vendidos
            top_medicamentos = self.controller.obtener_top_medicamentos(10)

            if not top_medicamentos:
                self.show_message("No hay datos de ventas disponibles para generar el reporte.")
                return

            # Crear gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 5))
            nombres = [med.nombre for med, _ in top_medicamentos]
            cantidades = [cantidad for _, cantidad in top_medicamentos]
            ax.bar(nombres, cantidades)
            ax.set_title("Top 10 Medicamentos Más Vendidos")
            ax.set_xlabel("Medicamento")
            ax.set_ylabel("Cantidad vendida")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Mostrar gráfico en la interfaz
            canvas = FigureCanvasTkAgg(fig, master=self.report_frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            self.show_error(f"Error al generar el reporte de medicamentos más vendidos: {str(e)}")

    def show_error(self, message):
        ctk.CTkMessagebox(title="Error", message=message, icon="cancel")

    def show_message(self, message):
        ctk.CTkMessagebox(title="Información", message=message, icon="info")