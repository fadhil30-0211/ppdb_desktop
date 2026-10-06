-- Buat database jika belum ada
CREATE DATABASE IF NOT EXISTS db_ppdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_ppdb;

-- Tabel Admin
CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- Insert akun admin default (Password: admin123)
INSERT INTO admin (username, password, nama_lengkap) 
VALUES ('admin', 'admin123', 'Administrator Utama')
ON DUPLICATE KEY UPDATE id=id;

-- Tabel Pendaftar
CREATE TABLE IF NOT EXISTS pendaftar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nisn VARCHAR(10) NOT NULL UNIQUE,
    nama_lengkap VARCHAR(100) NOT NULL,
    tempat_lahir VARCHAR(50) NOT NULL,
    tanggal_lahir DATE NOT NULL,
    jenis_kelamin ENUM('L', 'P') NOT NULL,
    alamat TEXT NOT NULL,
    asal_sekolah VARCHAR(100) NOT NULL,
    nilai_rata_rata DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    pilihan_jurusan VARCHAR(50) NOT NULL,
    nama_orang_tua VARCHAR(100) NOT NULL,
    no_hp VARCHAR(15) NOT NULL,
    status_seleksi ENUM('Diproses', 'Lulus', 'Tidak Lulus') DEFAULT 'Diproses',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;