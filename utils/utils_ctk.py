
class UtilsCTK:
    @staticmethod
    def clean_window(window):
        for widget in window.winfo_children():
            widget.destroy()