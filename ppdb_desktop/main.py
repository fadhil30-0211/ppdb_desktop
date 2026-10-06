import customtkinter as ctk
from modules.login import LoginWindow
from modules.dashboard import DashboardWindow

# Pengaturan Tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    """Controller Utama Aplikasi."""

    def __init__(self):
        super().__init__()

        self.title("Aplikasi PPDB Desktop - CustomTkinter & MySQL")
        self.geometry("1050x650")
        self.minsize(950, 580)

        self.current_frame = None
        self.show_login()

    def show_login(self):
        """Switch ke Halaman Login."""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = LoginWindow(self, on_login_success=self.show_dashboard)

    def show_dashboard(self, user_info):
        """Switch ke Halaman Dashboard."""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = DashboardWindow(self, user_info=user_info, on_logout=self.show_login)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()