import customtkinter as ctk
from tkinter import ttk, messagebox
from config.database import Database

class PendaftarView(ctk.CTkFrame):
    """Komponen Pengelolaan Data Pendaftar (CRUD)."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()
        self.selected_id = None

        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._create_form_section()
        self._create_table_section()
        self.load_data()

    def _create_form_section(self):
        """Formulir Input Data Pendaftar."""
        self.form_frame = ctk.CTkScrollableFrame(self, width=320, label_text="Form Data Pendaftar")
        self.form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        ctk.CTkLabel(self.form_frame, text="NISN:", anchor="w").pack(fill="x", pady=(5, 0))
        self.ent_nisn = ctk.CTkEntry(self.form_frame, placeholder_text="10 Digit NISN")
        self.ent_nisn.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Nama Lengkap:", anchor="w").pack(fill="x")
        self.ent_nama = ctk.CTkEntry(self.form_frame, placeholder_text="Nama Pendaftar")
        self.ent_nama.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Tempat Lahir:", anchor="w").pack(fill="x")
        self.ent_tempat_lahir = ctk.CTkEntry(self.form_frame, placeholder_text="Kota Lahir")
        self.ent_tempat_lahir.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Tanggal Lahir (YYYY-MM-DD):", anchor="w").pack(fill="x")
        self.ent_tgl_lahir = ctk.CTkEntry(self.form_frame, placeholder_text="2006-05-20")
        self.ent_tgl_lahir.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Jenis Kelamin:", anchor="w").pack(fill="x")
        self.cmb_jk = ctk.CTkOptionMenu(self.form_frame, values=["L", "P"])
        self.cmb_jk.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Asal Sekolah:", anchor="w").pack(fill="x")
        self.ent_sekolah = ctk.CTkEntry(self.form_frame, placeholder_text="SMP / MTs asal")
        self.ent_sekolah.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Nilai Rata-rata:", anchor="w").pack(fill="x")
        self.ent_nilai = ctk.CTkEntry(self.form_frame, placeholder_text="Contoh: 85.50")
        self.ent_nilai.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Pilihan Jurusan:", anchor="w").pack(fill="x")
        self.cmb_jurusan = ctk.CTkOptionMenu(
            self.form_frame, 
            values=["Teknik Komputer & Jaringan", "Rekayasa Perangkat Lunak", "Multi Media", "Akuntansi"]
        )
        self.cmb_jurusan.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Nama Orang Tua / Wali:", anchor="w").pack(fill="x")
        self.ent_ortu = ctk.CTkEntry(self.form_frame, placeholder_text="Nama Ayah/Ibu")
        self.ent_ortu.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="No. HP / WhatsApp:", anchor="w").pack(fill="x")
        self.ent_hp = ctk.CTkEntry(self.form_frame, placeholder_text="08123456789")
        self.ent_hp.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(self.form_frame, text="Alamat Lengkap:", anchor="w").pack(fill="x")
        self.ent_alamat = ctk.CTkEntry(self.form_frame, placeholder_text="Alamat domisili")
        self.ent_alamat.pack(fill="x", pady=(0, 15))

        self.btn_simpan = ctk.CTkButton(self.form_frame, text="Simpan Data", command=self.save_data)
        self.btn_simpan.pack(fill="x", pady=5)

        self.btn_clear = ctk.CTkButton(
            self.form_frame, 
            text="Reset Form", 
            fg_color="gray", 
            hover_color="darkgray", 
            command=self.clear_form
        )
        self.btn_clear.pack(fill="x", pady=5)

    def _create_table_section(self):
        """Tabel Treeview Data Pendaftar."""
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=0, column=1, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e", foreground="white", rowheight=25, fieldbackground="#2a2d2e")
        style.map("Treeview", background=[("selected", "#1f538d")])

        columns = ("id", "nisn", "nama", "sekolah", "nilai", "jurusan", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("nisn", text="NISN")
        self.tree.heading("nama", text="Nama Lengkap")
        self.tree.heading("sekolah", text="Asal Sekolah")
        self.tree.heading("nilai", text="Nilai")
        self.tree.heading("jurusan", text="Jurusan")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("nisn", width=90)
        self.tree.column("nama", width=150)
        self.tree.column("sekolah", width=120)
        self.tree.column("nilai", width=60, anchor="center")
        self.tree.column("jurusan", width=140)
        self.tree.column("status", width=90, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_row)

        self.action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        self.action_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        self.btn_hapus = ctk.CTkButton(
            self.action_frame, 
            text="Hapus Data Terpilih", 
            fg_color="#D32F2F", 
            hover_color="#B71C1C", 
            command=self.delete_data
        )
        self.btn_hapus.pack(side="right")

    def load_data(self):
        """Fetch & Tampilkan Seluruh Data Pendaftar."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = self.db.fetch_all("SELECT * FROM pendaftar ORDER BY id DESC")
        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["nisn"], r["nama_lengkap"], r["asal_sekolah"], 
                r["nilai_rata_rata"], r["pilihan_jurusan"], r["status_seleksi"]
            ))

    def on_select_row(self, event):
        """Select & Load ke Form Input."""
        selected = self.tree.selection()
        if not selected:
            return

        row_id = self.tree.item(selected[0])["values"][0]
        pendaftar = self.db.fetch_one("SELECT * FROM pendaftar WHERE id = %s", (row_id,))
        if pendaftar:
            self.selected_id = pendaftar["id"]
            self.clear_form()

            self.ent_nisn.insert(0, pendaftar["nisn"])
            self.ent_nama.insert(0, pendaftar["nama_lengkap"])
            self.ent_tempat_lahir.insert(0, pendaftar["tempat_lahir"])
            self.ent_tgl_lahir.insert(0, str(pendaftar["tanggal_lahir"]))
            self.cmb_jk.set(pendaftar["jenis_kelamin"])
            self.ent_sekolah.insert(0, pendaftar["asal_sekolah"])
            self.ent_nilai.insert(0, str(pendaftar["nilai_rata_rata"]))
            self.cmb_jurusan.set(pendaftar["pilihan_jurusan"])
            self.ent_ortu.insert(0, pendaftar["nama_orang_tua"])
            self.ent_hp.insert(0, pendaftar["no_hp"])
            self.ent_alamat.insert(0, pendaftar["alamat"])

            self.btn_simpan.configure(text="Perbarui Data")

    def clear_form(self):
        """Reset Seluruh Form Input."""
        self.selected_id = None
        self.ent_nisn.delete(0, "end")
        self.ent_nama.delete(0, "end")
        self.ent_tempat_lahir.delete(0, "end")
        self.ent_tgl_lahir.delete(0, "end")
        self.ent_sekolah.delete(0, "end")
        self.ent_nilai.delete(0, "end")
        self.ent_ortu.delete(0, "end")
        self.ent_hp.delete(0, "end")
        self.ent_alamat.delete(0, "end")
        self.btn_simpan.configure(text="Simpan Data")

    def save_data(self):
        """Insert atau Update Data Pendaftar."""
        nisn = self.ent_nisn.get().strip()
        nama = self.ent_nama.get().strip()
        tmpt = self.ent_tempat_lahir.get().strip()
        tgl = self.ent_tgl_lahir.get().strip()
        jk = self.cmb_jk.get()
        sekolah = self.ent_sekolah.get().strip()
        nilai = self.ent_nilai.get().strip()
        jurusan = self.cmb_jurusan.get()
        ortu = self.ent_ortu.get().strip()
        hp = self.ent_hp.get().strip()
        alamat = self.ent_alamat.get().strip()

        if not (nisn and nama and tmpt and tgl and sekolah and nilai and ortu and hp):
            messagebox.showwarning("Form Kosong", "Semua kolom wajib diisi!")
            return

        try:
            nilai_float = float(nilai)
        except ValueError:
            messagebox.showerror("Format Salah", "Nilai rata-rata harus berupa angka!")
            return

        if self.selected_id:
            sql = """
                UPDATE pendaftar 
                SET nisn=%s, nama_lengkap=%s, tempat_lahir=%s, tanggal_lahir=%s, jenis_kelamin=%s,
                    asal_sekolah=%s, nilai_rata_rata=%s, pilihan_jurusan=%s, nama_orang_tua=%s,
                    no_hp=%s, alamat=%s
                WHERE id=%s
            """
            params = (nisn, nama, tmpt, tgl, jk, sekolah, nilai_float, jurusan, ortu, hp, alamat, self.selected_id)
            if self.db.execute_query(sql, params):
                messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        else:
            sql = """
                INSERT INTO pendaftar 
                (nisn, nama_lengkap, tempat_lahir, tanggal_lahir, jenis_kelamin, asal_sekolah, nilai_rata_rata, pilihan_jurusan, nama_orang_tua, no_hp, alamat)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (nisn, nama, tmpt, tgl, jk, sekolah, nilai_float, jurusan, ortu, hp, alamat)
            if self.db.execute_query(sql, params):
                messagebox.showinfo("Sukses", "Data pendaftar berhasil ditambahkan!")

        self.clear_form()
        self.load_data()

    def delete_data(self):
        """Hapus Record Terpilih."""
        if not self.selected_id:
            messagebox.showwarning("Pilih Data", "Pilih data pendaftar pada tabel terlebih dahulu!")
            return

        if messagebox.askyesno("Konfirmasi Hapus", "Yakin ingin menghapus data ini?"):
            sql = "DELETE FROM pendaftar WHERE id = %s"
            if self.db.execute_query(sql, (self.selected_id,)):
                messagebox.showinfo("Sukses", "Data berhasil dihapus!")
                self.clear_form()
                self.load_data()