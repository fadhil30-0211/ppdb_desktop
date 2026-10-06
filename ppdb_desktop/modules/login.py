import customtkinter as ctk
from tkinter import messagebox
from config.database import Database

class LoginWindow(ctk.CTkFrame):
    """Komponen Antarmuka Login Admin Modern."""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.db = Database()

        self.pack(fill="both", expand=True)

        # Container Kartu Login
        self.card = ctk.CTkFrame(self, corner_radius=15, width=380, height=440)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Judul & Subjudul
        self.lbl_title = ctk.CTkLabel(
            self.card, 
            text="SYSTEM PPDB", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_title.pack(pady=(35, 5))

        self.lbl_subtitle = ctk.CTkLabel(
            self.card, 
            text="Silakan login untuk mengakses dashboard", 
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.lbl_subtitle.pack(pady=(0, 25))

        # Input Fields
        self.entry_username = ctk.CTkEntry(
            self.card, 
            placeholder_text="Username", 
            width=300, 
            height=40,
            corner_radius=8
        )
        self.entry_username.pack(pady=10)

        self.entry_password = ctk.CTkEntry(
            self.card, 
            placeholder_text="Password", 
            show="*", 
            width=300, 
            height=40,
            corner_radius=8
        )
        self.entry_password.pack(pady=10)

        # Tombol Login
        self.btn_login = ctk.CTkButton(
            self.card, 
            text="Masuk ke Sistem", 
            width=300, 
            height=40, 
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.handle_login
        )
        self.btn_login.pack(pady=(20, 10))

    def handle_login(self):
        """Proses Autentikasi Admin ke MySQL."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return

        query = "SELECT * FROM admin WHERE username = %s AND password = %s"
        admin = self.db.fetch_one(query, (username, password))

        if admin:
            messagebox.showinfo("Berhasil", f"Selamat datang, {admin['nama_lengkap']}!")
            self.on_login_success(admin)
        else:
            messagebox.showerror("Gagal Login", "Username atau password salah!")