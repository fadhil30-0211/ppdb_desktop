import customtkinter as ctk
from tkinter import ttk, messagebox
from config.database import Database

class SeleksiView(ctk.CTkFrame):
    """Komponen Live Search, Filtering, dan Seleksi Otomatis."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()

        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._create_filter_bar()
        self._create_seleksi_bar()
        self._create_table_section()
        self.load_data()

    def _create_filter_bar(self):
        """Bilah Pencarian & Filter Dropdown."""
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))

        ctk.CTkLabel(self.filter_frame, text="🔍 Cari:").pack(side="left", padx=(15, 5), pady=10)
        self.ent_search = ctk.CTkEntry(self.filter_frame, placeholder_text="NISN atau Nama...", width=180)
        self.ent_search.pack(side="left", padx=5, pady=10)
        self.ent_search.bind("<KeyRelease>", lambda e: self.load_data())

        ctk.CTkLabel(self.filter_frame, text="Jurusan:").pack(side="left", padx=(15, 5), pady=10)
        self.cmb_filter_jurusan = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["Semua", "Teknik Komputer & Jaringan", "Rekayasa Perangkat Lunak", "Multi Media", "Akuntansi"],
            command=lambda v: self.load_data()
        )
        self.cmb_filter_jurusan.pack(side="left", padx=5, pady=10)

        ctk.CTkLabel(self.filter_frame, text="Status:").pack(side="left", padx=(15, 5), pady=10)
        self.cmb_filter_status = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["Semua", "Diproses", "Lulus", "Tidak Lulus"],
            command=lambda v: self.load_data()
        )
        self.cmb_filter_status.pack(side="left", padx=5, pady=10)

        self.btn_reset = ctk.CTkButton(
            self.filter_frame, 
            text="Reset", 
            width=70, 
            fg_color="gray", 
            hover_color="darkgray",
            command=self.reset_filter
        )
        self.btn_reset.pack(side="left", padx=10, pady=10)

    def _create_seleksi_bar(self):
        """Panel Seleksi Otomatis Passing Grade."""
        self.seleksi_frame = ctk.CTkFrame(self)
        self.seleksi_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))

        ctk.CTkLabel(self.seleksi_frame, text="⚙️ Auto Seleksi (Passing Grade):", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(15, 5), pady=10)
        
        ctk.CTkLabel(self.seleksi_frame, text="Nilai Min:").pack(side="left", padx=5, pady=10)
        self.ent_min_score = ctk.CTkEntry(self.seleksi_frame, placeholder_text="75.00", width=80)
        self.ent_min_score.pack(side="left", padx=5, pady=10)
        self.ent_min_score.insert(0, "75.00")

        self.btn_run_seleksi = ctk.CTkButton(
            self.seleksi_frame, 
            text="Jalankan Seleksi Otomatis", 
            fg_color="#2E7D32", 
            hover_color="#1B5E20",
            command=self.run_auto_selection
        )
        self.btn_run_seleksi.pack(side="left", padx=15, pady=10)

    def _create_table_section(self):
        """Tabel Hasil Seleksi Pendaftar."""
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=2, column=0, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        columns = ("id", "nisn", "nama", "sekolah", "nilai", "jurusan", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nisn", text="NISN")
        self.tree.heading("nama", text="Nama Lengkap")
        self.tree.heading("sekolah", text="Asal Sekolah")
        self.tree.heading("nilai", text="Nilai Rata-rata")
        self.tree.heading("jurusan", text="Jurusan")
        self.tree.heading("status", text="Status Seleksi")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nisn", width=100)
        self.tree.column("nama", width=180)
        self.tree.column("sekolah", width=150)
        self.tree.column("nilai", width=100, anchor="center")
        self.tree.column("jurusan", width=160)
        self.tree.column("status", width=110, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Tombol Status Manual
        self.manual_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.manual_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        ctk.CTkLabel(self.manual_frame, text="Ubah Status Manual Data Terpilih:").pack(side="left", padx=5)

        self.btn_pass = ctk.CTkButton(
            self.manual_frame, text="Set Lulus", fg_color="#2E7D32", hover_color="#1B5E20", width=100,
            command=lambda: self.update_manual_status("Lulus")
        )
        self.btn_pass.pack(side="left", padx=5)

        self.btn_fail = ctk.CTkButton(
            self.manual_frame, text="Set Tidak Lulus", fg_color="#C62828", hover_color="#8E0000", width=110,
            command=lambda: self.update_manual_status("Tidak Lulus")
        )
        self.btn_fail.pack(side="left", padx=5)

    def reset_filter(self):
        """Mereset Seluruh Parameter Search & Filter."""
        self.ent_search.delete(0, "end")
        self.cmb_filter_jurusan.set("Semua")
        self.cmb_filter_status.set("Semua")
        self.load_data()

    def load_data(self):
        """Load Data Dinamis Menurut Pencarian."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = f"%{self.ent_search.get().strip()}%"
        jurusan = self.cmb_filter_jurusan.get()
        status = self.cmb_filter_status.get()

        query = "SELECT * FROM pendaftar WHERE (nisn LIKE %s OR nama_lengkap LIKE %s)"
        params = [keyword, keyword]

        if jurusan != "Semua":
            query += " AND pilihan_jurusan = %s"
            params.append(jurusan)

        if status != "Semua":
            query += " AND status_seleksi = %s"
            params.append(status)

        query += " ORDER BY nilai_rata_rata DESC"

        rows = self.db.fetch_all(query, tuple(params))
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["nisn"], r["nama_lengkap"], r["asal_sekolah"], 
                r["nilai_rata_rata"], r["pilihan_jurusan"], r["status_seleksi"]
            ))

    def run_auto_selection(self):
        """Kalkulasi Kelulusan Massal."""
        try:
            min_score = float(self.ent_min_score.get().strip())
        except ValueError:
            messagebox.showerror("Error Format", "Nilai minimum harus berupa angka!")
            return

        if not messagebox.askyesno("Konfirmasi Seleksi", f"Jalankan seleksi otomatis dengan Passing Grade >= {min_score}?"):
            return

        self.db.execute_query("UPDATE pendaftar SET status_seleksi = 'Lulus' WHERE nilai_rata_rata >= %s", (min_score,))
        self.db.execute_query("UPDATE pendaftar SET status_seleksi = 'Tidak Lulus' WHERE nilai_rata_rata < %s", (min_score,))

        messagebox.showinfo("Seleksi Selesai", "Status kelulusan berhasil dikalkulasi!")
        self.load_data()

    def update_manual_status(self, new_status):
        """Ubah Status Secara Manual pada Tabel."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih data pendaftar pada tabel terlebih dahulu!")
            return

        row_id = self.tree.item(selected[0])["values"][0]
        if self.db.execute_query("UPDATE pendaftar SET status_seleksi = %s WHERE id = %s", (new_status, row_id)):
            messagebox.showinfo("Berhasil", f"Status berhasil diubah menjadi '{new_status}'!")
            self.load_data()