class ViewManager:
    def __init__(self, master):
        self.master = master
        self.current_view = None

    def show_view(self, view_class, *args, **kwargs):
        """Destruye la vista actual y muestra una nueva vista."""
        self.clear_current_view()  # Eliminar la vista actual
        self.current_view = view_class(self.master, *args, **kwargs)
        self.current_view.pack(fill="both", expand=True)

    def clear_current_view(self):
        """Elimina la vista actual si existe."""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
