import customtkinter as ctk
from modules.pendaftar import PendaftarView
from modules.seleksi import SeleksiView
from modules.laporan import LaporanView

class DashboardWindow(ctk.CTkFrame):
    """Kerangka Utama Dashboard dan Panel Navigasi."""

    def __init__(self, parent, user_info, on_logout):
        super().__init__(parent)
        self.parent = parent
        self.user_info = user_info
        self.on_logout = on_logout

        self.pack(fill="both", expand=True)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_sidebar()
        self._create_content_area()
        self.switch_view("pendaftar")

    def _create_sidebar(self):
        """Membuat Sidebar Kiri."""
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.lbl_logo = ctk.CTkLabel(
            self.sidebar, 
            text="PPDB Admin", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.lbl_user = ctk.CTkLabel(
            self.sidebar, 
            text=f"👤 {self.user_info['nama_lengkap']}", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_user.grid(row=1, column=0, padx=20, pady=(0, 20))

        self.btn_nav_pendaftar = ctk.CTkButton(
            self.sidebar, 
            text="Data Pendaftar", 
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=lambda: self.switch_view("pendaftar")
        )
        self.btn_nav_pendaftar.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.btn_nav_seleksi = ctk.CTkButton(
            self.sidebar, 
            text="Seleksi & Status", 
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=lambda: self.switch_view("seleksi")
        )
        self.btn_nav_seleksi.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.btn_nav_laporan = ctk.CTkButton(
            self.sidebar, 
            text="Laporan & Ekspor", 
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=lambda: self.switch_view("laporan")
        )
        self.btn_nav_laporan.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.btn_logout = ctk.CTkButton(
            self.sidebar, 
            text="Keluar / Logout", 
            fg_color="#D32F2F", 
            hover_color="#B71C1C",
            command=self.on_logout
        )
        self.btn_logout.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

    def _create_content_area(self):
        """Kontainer Utama."""
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def switch_view(self, view_name):
        """Pergantian Tampilan Modul Dilihat dari Sidebar."""
        for widget in self.main_content.winfo_children():
            widget.destroy()

        if view_name == "pendaftar":
            PendaftarView(self.main_content)
        elif view_name == "seleksi":
            SeleksiView(self.main_content)
        elif view_name == "laporan":
            LaporanView(self.main_content)