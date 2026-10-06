import mysql.connector
from mysql.connector import Error

class Database:
    """Kelas untuk mengelola koneksi dan query database MySQL."""
    
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""  # Ubah jika XAMPP/MySQL Anda menggunakan password
        self.database = "db_ppdb"
        self.connection = None

    def connect(self):
        """Membuka koneksi ke database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"[ERROR] Gagal terhubung ke database: {e}")
            return None

    def disconnect(self):
        """Meninggalkam/menutup koneksi database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        """Menjalankan query INSERT, UPDATE, DELETE."""
        conn = self.connect()
        if not conn:
            return False
        
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True
        except Error as e:
            print(f"[ERROR] Query Gagal: {e}")
            return False
        finally:
            cursor.close()
            self.disconnect()

    def fetch_all(self, query, params=None):
        """Mengambil seluruh baris data dari query SELECT."""
        conn = self.connect()
        if not conn:
            return []
        
        cursor = conn.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"[ERROR] Fetch Gagal: {e}")
            return []
        finally:
            cursor.close()
            self.disconnect()

    def fetch_one(self, query, params=None):
        """Mengambil satu baris data dari query SELECT."""
        conn = self.connect()
        if not conn:
            return None
        
        cursor = conn.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"[ERROR] Fetch One Gagal: {e}")
            return None
        finally:
            cursor.close()
            self.disconnect()