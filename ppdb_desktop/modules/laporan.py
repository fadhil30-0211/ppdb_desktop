import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config.database import Database

class LaporanView(ctk.CTkFrame):
    """Komponen Ekspor Laporan Excel & Bukti Pendaftaran PDF."""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.db = Database()

        self.pack(fill="both", expand=True)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._create_toolbar()
        self._create_table_section()
        self.load_data()

    def _create_toolbar(self):
        """Baris Tombol Aksi Laporan."""
        self.toolbar = ctk.CTkFrame(self)
        self.toolbar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 10))

        ctk.CTkLabel(self.toolbar, text="Filter Jurusan:").pack(side="left", padx=(15, 5), pady=10)
        self.cmb_filter = ctk.CTkOptionMenu(
            self.toolbar,
            values=["Semua", "Teknik Komputer & Jaringan", "Rekayasa Perangkat Lunak", "Multi Media", "Akuntansi"],
            command=lambda v: self.load_data()
        )
        self.cmb_filter.pack(side="left", padx=5, pady=10)

        self.btn_export_excel = ctk.CTkButton(
            self.toolbar,
            text="📊 Ekspor ke Excel",
            fg_color="#1D6F42",
            hover_color="#155231",
            command=self.export_to_excel
        )
        self.btn_export_excel.pack(side="left", padx=10, pady=10)

        self.btn_print_pdf = ctk.CTkButton(
            self.toolbar,
            text="📄 Cetak Bukti PDF",
            fg_color="#0277BD",
            hover_color="#01579B",
            command=self.export_to_pdf
        )
        self.btn_print_pdf.pack(side="left", padx=5, pady=10)

    def _create_table_section(self):
        """Tabel Pratinjau Laporan."""
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, sticky="nsew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

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
        self.tree.column("nisn", width=100)
        self.tree.column("nama", width=180)
        self.tree.column("sekolah", width=150)
        self.tree.column("nilai", width=80, anchor="center")
        self.tree.column("jurusan", width=160)
        self.tree.column("status", width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def load_data(self):
        """Load Data untuk Pratinjau Laporan."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        filter_jurusan = self.cmb_filter.get()
        if filter_jurusan == "Semua":
            rows = self.db.fetch_all("SELECT * FROM pendaftar ORDER BY id DESC")
        else:
            rows = self.db.fetch_all("SELECT * FROM pendaftar WHERE pilihan_jurusan = %s ORDER BY id DESC", (filter_jurusan,))

        for r in rows:
            self.tree.insert("", "end", values=(
                r["id"], r["nisn"], r["nama_lengkap"], r["asal_sekolah"],
                r["nilai_rata_rata"], r["pilihan_jurusan"], r["status_seleksi"]
            ))

    def export_to_excel(self):
        """Generasi File Spreadsheet Excel (.xlsx)."""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Simpan Laporan Excel"
        )
        if not filepath:
            return

        wb = Workbook()
        ws = wb.active
        ws.title = "Rekapitulasi PPDB"

        headers = ["ID", "NISN", "Nama Lengkap", "Tempat Lahir", "Tgl Lahir", "JK", "Asal Sekolah", "Nilai", "Jurusan", "No HP", "Status"]
        ws.append(headers)

        filter_jurusan = self.cmb_filter.get()
        if filter_jurusan == "Semua":
            rows = self.db.fetch_all("SELECT * FROM pendaftar ORDER BY id ASC")
        else:
            rows = self.db.fetch_all("SELECT * FROM pendaftar WHERE pilihan_jurusan = %s ORDER BY id ASC", (filter_jurusan,))

        for r in rows:
            ws.append([
                r["id"], r["nisn"], r["nama_lengkap"], r["tempat_lahir"],
                str(r["tanggal_lahir"]), r["jenis_kelamin"], r["asal_sekolah"],
                float(r["nilai_rata_rata"]), r["pilihan_jurusan"], r["no_hp"], r["status_seleksi"]
            ])

        try:
            wb.save(filepath)
            messagebox.showinfo("Berhasil", "Data berhasil diekspor ke file Excel!")
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal menyimpan file Excel: {e}")

    def export_to_pdf(self):
        """Generasi File Kartu Bukti PDF."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Data", "Pilih pendaftar pada tabel untuk mencetak PDF!")
            return

        row_id = self.tree.item(selected[0])["values"][0]
        pendaftar = self.db.fetch_one("SELECT * FROM pendaftar WHERE id = %s", (row_id,))

        if not pendaftar:
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Documents", "*.pdf")],
            initialfile=f"Bukti_PPDB_{pendaftar['nisn']}.pdf",
            title="Simpan Bukti Pendaftaran PDF"
        )
        if not filepath:
            return

        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, 750, "KARTU BUKTI PENDAFTARAN PPDB")
            c.setFont("Helvetica", 10)
            c.drawString(200, 735, "Tahun Ajaran Resmi Penerimaan Siswa Baru")
            c.line(50, 720, 550, 720)

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 680, "DATA CALON SISWA:")
            
            c.setFont("Helvetica", 11)
            y = 650
            details = [
                ("NISN", pendaftar["nisn"]),
                ("Nama Lengkap", pendaftar["nama_lengkap"]),
                ("TTL", f"{pendaftar['tempat_lahir']}, {pendaftar['tanggal_lahir']}"),
                ("Jenis Kelamin", "Laki-laki" if pendaftar["jenis_kelamin"] == "L" else "Perempuan"),
                ("Asal Sekolah", pendaftar["asal_sekolah"]),
                ("Nilai Rata-rata", str(pendaftar["nilai_rata_rata"])),
                ("Pilihan Jurusan", pendaftar["pilihan_jurusan"]),
                ("Nama Orang Tua", pendaftar["nama_orang_tua"]),
                ("No. HP / WA", pendaftar["no_hp"]),
                ("Status Seleksi", pendaftar["status_seleksi"].upper())
            ]

            for label, value in details:
                c.drawString(70, y, f"{label:<20} : {value}")
                y -= 25

            c.line(50, y - 10, 550, y - 10)
            c.setFont("Helvetica-Oblique", 9)
            c.drawString(50, y - 30, "* Simpan bukti ini sebagai syarat verifikasi pendaftaran ulang.")

            c.save()
            messagebox.showinfo("Berhasil", "Kartu Bukti Pendaftaran PDF berhasil diterbitkan!")
        except Exception as e:
            messagebox.showerror("Gagal", f"Gagal membuat dokumen PDF: {e}")