from tkinter import messagebox


class Notifications:

    def __init__(self):
        self.notifications = messagebox

    def show_info(self, title, message):
        self.notifications.showinfo(title, message)

    def show_error(self, title, message):
        self.notifications.showerror(title, message)

    def show_confirmation(self, title, message, **kwargs):
        return self.notifications.askyesno(title, message, **kwargs)
