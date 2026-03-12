import sys
import mysql.connector
from datetime import date, datetime, timedelta

# --- IMPORT LIBRARY UI ---
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel,
                               QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt, QDate, QTimer

# --- LIBRARY PDF (Pastikan sudah install: pip install reportlab) ---
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# --- IMPORT FILE UI ---
# Pastikan semua file .py hasil convert UI ada di folder yang sama
from Login import Ui_MainWindow as Ui_LoginWindow
from DashboardAdmin import Ui_MainWindow as Ui_AdminWindow
from Register import Ui_MainWindow as Ui_RegisterWindow
from DataKaryawan import Ui_MainWindow as Ui_DataKaryawanWindow
from Jabatan import Ui_MainWindow as Ui_JabatanWindow
from AbsensiAdmin import Ui_MainWindow as Ui_AbsensiWindow
from LaporanGaji import Ui_MainWindow as Ui_LaporanGajiWindow
from ValidasiGaji import Ui_MainWindow as Ui_ValidasiGajiWindow
from ArsipNonaktif import Ui_MainWindow as Ui_ArsipNonaktifWindow
from AbsensiKaryawan import Ui_MainWindow as Ui_AbsensiKaryawanWindow
from PengajuanCuti import Ui_MainWindow as Ui_PengajuanCutiWindow
from SlipGaji import Ui_MainWindow as Ui_SlipGajiWindow
from RiwayatCuti import Ui_MainWindow as Ui_RiwayatCutiWindow

# --- KONEKSI DATABASE ---
def create_connection():
    try:
        # Default XAMPP: user='root', password=''
        return mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="", 
            database="bakery_management"
        )
    except mysql.connector.Error as err:
        return None

# --- INISIALISASI DATABASE (Hanya dijalankan sekali di awal) ---
def init_all_tables():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # 1. Tabel Jabatan
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jabatan (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama_jabatan VARCHAR(50) NOT NULL UNIQUE,
                    gaji_pokok DOUBLE NOT NULL,
                    tunjangan_jabatan DOUBLE NOT NULL,
                    tunjangan_kehadiran DOUBLE NOT NULL
                )
            """)
            
            # 2. Tabel Karyawan
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS karyawan (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama_lengkap VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    jabatan VARCHAR(50) NOT NULL,
                    status_kerja VARCHAR(20) NOT NULL,
                    status_akun VARCHAR(20) DEFAULT 'Aktif',
                    tanggal_gabung DATE
                )
            """)

            # 3. Tabel Absensi
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS absensi (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    karyawan_id INT,
                    tanggal DATE,
                    waktu_masuk TIME,
                    waktu_pulang TIME,
                    status VARCHAR(20), 
                    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE CASCADE
                )
            """)

            # 4. Tabel Cuti
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cuti (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    karyawan_id INT,
                    tanggal_mulai DATE,
                    jumlah_hari INT,
                    alasan TEXT,
                    status_validasi VARCHAR(20) DEFAULT 'Pending',
                    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE CASCADE
                )
            """)
            
            # 5. Tabel Gaji
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gaji (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    karyawan_id INT,
                    bulan INT,
                    tahun INT,
                    gaji_pokok DOUBLE,
                    total_tunjangan DOUBLE,
                    total_potongan DOUBLE,
                    total_gaji DOUBLE,
                    status_transfer VARCHAR(20) DEFAULT 'Pending',
                    status_validasi VARCHAR(20) DEFAULT 'Pending',
                    tanggal_transfer DATE,
                    bukti_transfer VARCHAR(255),
                    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE CASCADE
                )
            """)
            
            # Tambah kolom status_validasi jika belum ada
            try:
                cursor.execute("""
                    ALTER TABLE gaji ADD COLUMN status_validasi VARCHAR(20) DEFAULT 'Pending'
                """)
            except mysql.connector.Error:
                pass  # Kolom sudah ada
            
            # --- DATA DUMMY (Jika Kosong) ---
            cursor.execute("SELECT COUNT(*) FROM jabatan")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran) VALUES ('Admin', 4000000, 500000, 200000), ('Kasir', 3000000, 250000, 150000), ('Baker', 3500000, 300000, 150000)")
            
            cursor.execute("SELECT COUNT(*) FROM karyawan")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES ('Super Admin', 'admin@toko.com', 'admin123', 'Admin', 'Tetap', 'Aktif', %s)", (date.today(),))
                cursor.execute("INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES ('Sinta Andini', 'sinta@toko.com', 'sinta123', 'Kasir', 'Kontrak', 'Aktif', %s)", (date.today(),))

            conn.commit()
            print("Database initialized.")
        except mysql.connector.Error as e:
            print(f"Database Init Error: {e}")
        finally:
            conn.close()

def generate_gaji_otomatis(bulan, tahun):
    conn = create_connection()
    if not conn:
        return False, "Koneksi database gagal"

    try:
        cur = conn.cursor()

        # Ambil karyawan aktif
        cur.execute("""
            SELECT k.id, j.gaji_pokok, j.tunjangan_jabatan, j.tunjangan_kehadiran
            FROM karyawan k
            JOIN jabatan j ON k.jabatan = j.nama_jabatan
            WHERE k.status_akun = 'Aktif'
        """)
        karyawan = cur.fetchall()

        for k_id, gaji_pokok, tunj_jabatan, tunj_hadir in karyawan:

            # Cegah duplikasi
            cur.execute("""
                SELECT id FROM gaji
                WHERE karyawan_id=%s AND bulan=%s AND tahun=%s
            """, (k_id, bulan, tahun))
            if cur.fetchone():
                continue

            # Hitung hadir
            cur.execute("""
                SELECT COUNT(*) FROM absensi
                WHERE karyawan_id=%s
                AND status='Hadir'
                AND MONTH(tanggal)=%s
                AND YEAR(tanggal)=%s
            """, (k_id, bulan, tahun))
            hadir = cur.fetchone()[0]

            # Hitung cuti disetujui
            cur.execute("""
                SELECT IFNULL(SUM(jumlah_hari),0)
                FROM cuti
                WHERE karyawan_id=%s
                AND status_validasi='Disetujui'
                AND MONTH(tanggal_mulai)=%s
                AND YEAR(tanggal_mulai)=%s
            """, (k_id, bulan, tahun))
            cuti = cur.fetchone()[0]

            # Asumsi 26 hari kerja
            absen = max(0, 26 - hadir - cuti)
            potongan = (gaji_pokok / 26) * absen

            # Tunjangan hadir hanya kalau >=20 hari
            tunj_kehadiran = tunj_hadir if hadir >= 20 else 0
            total_tunjangan = tunj_jabatan + tunj_kehadiran

            total_gaji = gaji_pokok + total_tunjangan - potongan

            # Insert gaji
            cur.execute("""
                INSERT INTO gaji (
                    karyawan_id, bulan, tahun,
                    gaji_pokok, total_tunjangan,
                    total_potongan, total_gaji
                ) VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                k_id, bulan, tahun,
                gaji_pokok, total_tunjangan,
                potongan, total_gaji
            ))

        conn.commit()
        return True, "Gaji berhasil digenerate"

    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

# --- DIALOG CLASSES (Untuk Edit/Input) ---
class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Karyawan")
        self.resize(400, 350)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.input_nama = QLineEdit(self)
        self.input_email = QLineEdit(self)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        
        self.combo_jabatan = QComboBox(self)
        self.load_jabatan_combo()
        
        self.combo_status = QComboBox(self)
        self.combo_status.addItems(["Tetap", "Kontrak"])
        
        form.addRow("Nama Lengkap:", self.input_nama)
        form.addRow("Email:", self.input_email)
        form.addRow("Password:", self.input_password)
        form.addRow("Jabatan:", self.combo_jabatan)
        form.addRow("Status Kerja:", self.combo_status)
        
        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)
    
    def load_jabatan_combo(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nama_jabatan FROM jabatan")
                for row in cursor.fetchall():
                    self.combo_jabatan.addItem(row[0])
            except: pass
            finally: conn.close()
    
    def get_data(self):
        return {
            'nama': self.input_nama.text(),
            'email': self.input_email.text(),
            'password': self.input_password.text(),
            'jabatan': self.combo_jabatan.currentText(),
            'status_kerja': self.combo_status.currentText()
        }

# --- DIALOG CLASSES (Untuk Edit/Input) ---
class EditEmployeeDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Data Karyawan")
        self.resize(400, 300)
        self.data = data 
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.input_nama = QLineEdit(self)
        self.input_nama.setText(data['nama'])
        form.addRow("Nama Lengkap:", self.input_nama)
        
        self.combo_jabatan = QComboBox(self)
        self.load_jabatan_combo()
        self.combo_jabatan.setCurrentText(data['jabatan'])
        form.addRow("Jabatan:", self.combo_jabatan)
        
        self.combo_status_kerja = QComboBox(self)
        self.combo_status_kerja.addItems(["Tetap", "Kontrak"])
        self.combo_status_kerja.setCurrentText(data['status_kerja'])
        form.addRow("Status Kerja:", self.combo_status_kerja)
        
        self.combo_status_akun = QComboBox(self)
        self.combo_status_akun.addItems(["Aktif", "Nonaktif"])
        self.combo_status_akun.setCurrentText(data['status_akun'])
        form.addRow("Status Akun:", self.combo_status_akun)
        
        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def load_jabatan_combo(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT nama_jabatan FROM jabatan")
                for row in cursor.fetchall():
                    self.combo_jabatan.addItem(row[0])
            except: pass
            finally: conn.close()

    def get_updated_data(self):
        return {
            'nama': self.input_nama.text(),
            'jabatan': self.combo_jabatan.currentText(),
            'status_kerja': self.combo_status_kerja.currentText(),
            'status_akun': self.combo_status_akun.currentText()
        }

class JabatanDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Form Jabatan")
        self.resize(400, 250)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.input_nama = QLineEdit(self)
        self.input_gaji = QDoubleSpinBox(self)
        self.input_gaji.setRange(0, 1e9)
        self.input_gaji.setGroupSeparatorShown(True)
        
        self.input_tunj_jab = QDoubleSpinBox(self)
        self.input_tunj_jab.setRange(0, 1e9)
        self.input_tunj_jab.setGroupSeparatorShown(True)
        
        self.input_tunj_hadir = QDoubleSpinBox(self)
        self.input_tunj_hadir.setRange(0, 1e9)
        self.input_tunj_hadir.setGroupSeparatorShown(True)
        
        if data:
            self.input_nama.setText(data['nama'])
            self.input_gaji.setValue(float(data['gaji']))
            self.input_tunj_jab.setValue(float(data['tunj_jab']))
            self.input_tunj_hadir.setValue(float(data['tunj_hadir']))
            
        form.addRow("Nama Jabatan:", self.input_nama)
        form.addRow("Gaji Pokok:", self.input_gaji)
        form.addRow("Tunjangan Jabatan:", self.input_tunj_jab)
        form.addRow("Tunjangan Kehadiran:", self.input_tunj_hadir)
        
        layout.addLayout(form)
        btns = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def get_data(self):
        return {
            'nama': self.input_nama.text(),
            'gaji': self.input_gaji.value(),
            'tunj_jab': self.input_tunj_jab.value(),
            'tunj_hadir': self.input_tunj_hadir.value()
        }

# --- BASE WINDOW CLASS (Untuk navigasi umum) ---
class BaseWindow(QMainWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.previous_window = previous_window
    
    def setup_nav(self):
        """Setup tombol navigasi umum"""
        try:
            self.pushButton_2.clicked.connect(self.back_to_dashboard)
            if hasattr(self, 'pushButton_4'): self.pushButton_4.clicked.connect(self.open_data_karyawan)
            if hasattr(self, 'pushButton_3'): self.pushButton_3.clicked.connect(self.open_jabatan)
            if hasattr(self, 'pushButton'): self.pushButton.clicked.connect(self.open_absensi)
            if hasattr(self, 'pushButton_5'): self.pushButton_5.clicked.connect(self.open_laporan)
            if hasattr(self, 'pushButton_6'): self.pushButton_6.clicked.connect(self.open_validasi)
            if hasattr(self, 'pushButton_7'): self.pushButton_7.clicked.connect(self.open_arsip)
            if hasattr(self, 'pushButton_8'): self.pushButton_8.clicked.connect(self.handle_logout)
        except: pass
    
    def back_to_dashboard(self): 
        if self.previous_window: self.hide(); self.previous_window.show()
    def open_data_karyawan(self): 
        self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_jabatan(self): 
        self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_absensi(self): 
        self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_laporan(self): 
        self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_validasi(self): 
        self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): 
        self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def handle_logout(self): 
        self.close(); global window; window.show()

# --- WINDOW: ARSIP NONAKTIF ---
class ArsipNonaktifWindow(QMainWindow, Ui_ArsipNonaktifWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window
        self.setup_table()
        self.load_data()
        self.pushButton_7.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        
        self.pushButton_11.setText("Pulihkan (Aktifkan)")
        self.pushButton_10.setText("Hapus Permanen")
        
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_8.clicked.connect(self.handle_logout)
        
        self.pushButton_11.clicked.connect(self.restore_employee)
        self.pushButton_10.clicked.connect(self.delete_permanent)

    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nama_lengkap, jabatan, tanggal_gabung FROM karyawan WHERE status_akun='Nonaktif'")
                results = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for r, d in enumerate(results):
                    self.tableWidget.insertRow(r)
                    id_item = QTableWidgetItem(str(r + 1))
                    id_item.setData(Qt.UserRole, d[0])
                    self.tableWidget.setItem(r, 0, id_item)
                    self.tableWidget.setItem(r, 1, QTableWidgetItem(d[1]))
                    self.tableWidget.setItem(r, 2, QTableWidgetItem(d[2]))
                    self.tableWidget.setItem(r, 3, QTableWidgetItem(str(d[3]))) 
            finally: conn.close()

    def restore_employee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Pilih karyawan yang ingin dipulihkan.")
            return
        emp_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        nama = self.tableWidget.item(row, 1).text()
        if QMessageBox.question(self, "Konfirmasi", f"Aktifkan kembali '{nama}'?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE karyawan SET status_akun='Aktif' WHERE id=%s", (emp_id,))
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Karyawan dipulihkan.")
                    self.load_data()
                except: pass
                finally: conn.close()

    def delete_permanent(self):
        row = self.tableWidget.currentRow()
        if row < 0: return
        emp_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        if QMessageBox.warning(self, "Hapus Permanen", "Data akan hilang selamanya. Lanjutkan?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM karyawan WHERE id=%s", (emp_id,))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def open_data_karyawan(self): self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_jabatan(self): self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_absensi(self): self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_laporan(self): self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_validasi(self): self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()

# --- WINDOW: VALIDASI GAJI ---
class ValidasiGajiWindow(QMainWindow, Ui_ValidasiGajiWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window

        self.setup_table()
        self.load_data()

        self.pushButton_6.setStyleSheet(
            "background-color: #d6dc82; color: #262628; font-weight: bold;"
        )
        
        # Resize font pada label untuk keterbacaan
        self.setup_label_fonts()

        # NAVIGASI (LANGSUNG TUTUP WINDOW LAMA)
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_7.clicked.connect(self.open_arsip)
        self.pushButton_8.clicked.connect(self.handle_logout)

        # AKSI ADMIN
        if hasattr(self, 'pushButton_9'):  # Jika ada button generate
            self.pushButton_9.clicked.connect(self.generate_gaji_sekarang)
        self.pushButton_11.clicked.connect(self.validasi_gaji)
        self.pushButton_10.clicked.connect(self.approve_transfer)

    # ================= LABEL FONTS =================
    def setup_label_fonts(self):
        """Resize font pada semua label agar terbaca"""
        try:
            font = self.font()
            font.setPointSize(9)
            for widget in self.findChildren(QLabel):
                widget.setFont(font)
        except:
            pass

    # ================= TABLE =================
    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT g.id, k.nama_lengkap, g.bulan, g.tahun,
                       g.total_gaji, g.status_validasi
                FROM gaji g
                JOIN karyawan k ON g.karyawan_id = k.id
                ORDER BY g.status_validasi ASC, g.tahun DESC, g.bulan DESC
            """)
            data = cur.fetchall()

            self.tableWidget.setRowCount(0)
            for r, d in enumerate(data):
                self.tableWidget.insertRow(r)

                no = QTableWidgetItem(str(r + 1))
                no.setData(Qt.UserRole, d[0])

                self.tableWidget.setItem(r, 0, no)
                self.tableWidget.setItem(r, 1, QTableWidgetItem(d[1]))
                self.tableWidget.setItem(r, 2, QTableWidgetItem(f"{d[2]}/{d[3]}"))
                self.tableWidget.setItem(r, 3, QTableWidgetItem(f"Rp {d[4]:,.0f}"))
                
                # Tampilkan status_validasi dengan warna
                status_item = QTableWidgetItem(d[5])
                if d[5] == 'Valid':
                    status_item.setBackground(colors.HexColor('#90EE90') if hasattr(colors, 'HexColor') else None)
                self.tableWidget.setItem(r, 4, status_item)

        finally:
            conn.close()

    # ================= LOGIC ADMIN =================
    def generate_gaji_sekarang(self):
        """Generate gaji bulan ini untuk semua karyawan aktif"""
        if QMessageBox.question(
            self,
            "Konfirmasi Generate Gaji",
            f"Generate gaji bulan {date.today().strftime('%B %Y')} untuk semua karyawan aktif?",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return
        
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Koneksi database gagal")
            return

        try:
            bulan = date.today().month
            tahun = date.today().year
            cur = conn.cursor()
            generated = 0
            
            cur.execute("""
                SELECT k.id, j.gaji_pokok, j.tunjangan_jabatan, j.tunjangan_kehadiran
                FROM karyawan k
                JOIN jabatan j ON k.jabatan = j.nama_jabatan
                WHERE k.status_akun='Aktif'
            """)
            
            for k_id, gaji_pokok, tunj_jabatan, tunj_hadir in cur.fetchall():
                # Cek duplikasi
                cur.execute(
                    "SELECT id FROM gaji WHERE karyawan_id=%s AND bulan=%s AND tahun=%s",
                    (k_id, bulan, tahun)
                )
                if cur.fetchone():
                    continue
                
                # Hitung hadir
                cur.execute(
                    "SELECT COUNT(*) FROM absensi WHERE karyawan_id=%s AND MONTH(tanggal)=%s AND YEAR(tanggal)=%s",
                    (k_id, bulan, tahun)
                )
                hadir = cur.fetchone()[0] or 0
                
                # Hitung cuti disetujui
                cur.execute(
                    "SELECT IFNULL(SUM(jumlah_hari),0) FROM cuti WHERE karyawan_id=%s AND status_validasi='Disetujui' AND MONTH(tanggal_mulai)=%s AND YEAR(tanggal_mulai)=%s",
                    (k_id, bulan, tahun)
                )
                cuti = cur.fetchone()[0] or 0
                
                hari_absen = max(0, 26 - hadir - cuti)
                potongan = (gaji_pokok / 26) * hari_absen
                tunj_kehadiran = tunj_hadir if hadir >= 20 else 0
                total_tunjangan = tunj_jabatan + tunj_kehadiran
                total_gaji = gaji_pokok + total_tunjangan - potongan
                
                cur.execute(
                    "INSERT INTO gaji (karyawan_id, bulan, tahun, gaji_pokok, total_tunjangan, total_potongan, total_gaji, status_transfer) VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending')",
                    (k_id, bulan, tahun, gaji_pokok, total_tunjangan, potongan, total_gaji)
                )
                generated += 1
            
            conn.commit()
            QMessageBox.information(self, "Sukses", f"Generate {generated} gaji berhasil")
            self.load_data()
        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error", f"Generate gagal: {str(e)}")
        finally:
            conn.close()

    def validasi_gaji(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Data", "Pilih data gaji terlebih dahulu.")
            return

        gaji_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        current_status = self.tableWidget.item(row, 4).text()

        if current_status == 'Valid':
            QMessageBox.information(self, "Info", "Gaji ini sudah divalidasi oleh karyawan.")
            return

        if QMessageBox.question(
            self,
            "Konfirmasi Validasi Admin",
            "Validasi gaji ini?\nStatus akan menjadi 'Valid' dan karyawan mendapat bonus 5%.",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:

            conn = create_connection()
            try:
                cur = conn.cursor()
                cur.execute(
                    "UPDATE gaji SET status_validasi='Valid' WHERE id=%s",
                    (gaji_id,)
                )
                conn.commit()
                self.load_data()
                QMessageBox.information(self, "Sukses", "Gaji telah divalidasi dengan bonus 5%")
            finally:
                conn.close()

    def approve_transfer(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            return

        gaji_id = self.tableWidget.item(row, 0).data(Qt.UserRole)

        if QMessageBox.question(
            self,
            "Konfirmasi",
            "Tandai gaji sudah ditransfer?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:

            conn = create_connection()
            try:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE gaji
                    SET status_transfer='Sudah Transfer',
                        tanggal_transfer=%s
                    WHERE id=%s
                """, (date.today(), gaji_id))
                conn.commit()
                self.load_data()
            finally:
                conn.close()

    # ================= NAVIGASI =================
    def open_data_karyawan(self):
        self.close()
        self.win = DataKaryawanWindow(self.previous_window)
        self.win.show()

    def open_jabatan(self):
        self.close()
        self.win = JabatanWindow(self.previous_window)
        self.win.show()

    def open_absensi(self):
        self.close()
        self.win = AbsensiAdminWindow(self.previous_window)
        self.win.show()

    def open_laporan(self):
        self.close()
        self.win = LaporanGajiWindow(self.previous_window)
        self.win.show()

    def open_arsip(self):
        self.close()
        self.win = ArsipNonaktifWindow(self.previous_window)
        self.win.show()

    def back_to_dashboard(self):
        self.close()
        self.previous_window.load_dashboard_data()
        self.previous_window.show()

    def handle_logout(self):
        self.close()
        global window
        window.show()

# --- WINDOW: LAPORAN GAJI ---
class LaporanGajiWindow(QMainWindow, Ui_LaporanGajiWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window

        self.populate_year_combo()
        self.setup_table()
        self.comboBox.setCurrentText(str(date.today().year))

        self.pushButton_5.setStyleSheet(
            "background-color: #d6dc82; color: #262628; font-weight: bold;"
        )

        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)

        # NAVIGATION
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_7.clicked.connect(self.open_arsip)
        self.pushButton_8.clicked.connect(self.handle_logout)

        # ACTION
        self.pushButton_9.clicked.connect(self.handle_generate_gaji)  # GENERATE
        self.pushButton_10.clicked.connect(self.export_pdf)

        self.load_data()

    # =========================
    # SETUP
    # =========================
    def populate_year_combo(self):
        curr = date.today().year
        for y in range(curr+1, curr-5, -1):
            self.comboBox.addItem(str(y))

    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    # =========================
    # GENERATE GAJI OTOMATIS (DIPERBAIKI)
    # =========================
    def handle_generate_gaji(self):
        tahun = int(self.comboBox.currentText())
        bulan = date.today().month
        
        conn = create_connection()
        if not conn:
            QMessageBox.critical(self, "Error", "Koneksi database gagal")
            return

        try:
            cur = conn.cursor()
            generated_count = 0
            
            # Ambil semua karyawan aktif
            cur.execute("""
                SELECT k.id, k.nama_lengkap, j.gaji_pokok, j.tunjangan_jabatan, j.tunjangan_kehadiran
                FROM karyawan k
                JOIN jabatan j ON k.jabatan = j.nama_jabatan
                WHERE k.status_akun='Aktif'
            """)
            karyawans = cur.fetchall()

            for emp_data in karyawans:
                k_id, k_nama, gaji_pokok, tunj_jabatan, tunj_hadir = emp_data

                # CEGAH DUPLIKASI
                cur.execute("""
                    SELECT id FROM gaji
                    WHERE karyawan_id=%s AND bulan=%s AND tahun=%s
                """, (k_id, bulan, tahun))
                if cur.fetchone():
                    continue

                # HITUNG HADIR
                cur.execute("""
                    SELECT COUNT(*) FROM absensi
                    WHERE karyawan_id=%s
                    AND MONTH(tanggal)=%s
                    AND YEAR(tanggal)=%s
                """, (k_id, bulan, tahun))
                hadir = cur.fetchone()[0] or 0

                # HITUNG CUTI DISETUJUI
                cur.execute("""
                    SELECT IFNULL(SUM(jumlah_hari),0)
                    FROM cuti
                    WHERE karyawan_id=%s
                    AND status_validasi='Disetujui'
                    AND MONTH(tanggal_mulai)=%s
                    AND YEAR(tanggal_mulai)=%s
                """, (k_id, bulan, tahun))
                cuti = cur.fetchone()[0] or 0

                # PERHITUNGAN GAJI (26 hari kerja)
                hari_kerja = 26
                hari_absen = max(0, hari_kerja - hadir - cuti)
                gaji_per_hari = gaji_pokok / hari_kerja
                potongan = gaji_per_hari * hari_absen

                # TUNJANGAN
                tunj_kehadiran = tunj_hadir if hadir >= 20 else 0
                total_tunjangan = tunj_jabatan + tunj_kehadiran

                total_gaji = gaji_pokok + total_tunjangan - potongan

                # INSERT GAJI
                cur.execute("""
                    INSERT INTO gaji (
                        karyawan_id, bulan, tahun,
                        gaji_pokok, total_tunjangan,
                        total_potongan, total_gaji, status_transfer
                    ) VALUES (%s,%s,%s,%s,%s,%s,%s,'Pending')
                """, (
                    k_id, bulan, tahun,
                    gaji_pokok, total_tunjangan,
                    potongan, total_gaji
                ))
                generated_count += 1

            conn.commit()
            msg = f"Sukses generate gaji untuk {generated_count} karyawan (Bulan {bulan}/{tahun})"
            QMessageBox.information(self, "Sukses", msg)
            self.load_data()

        except Exception as e:
            conn.rollback()
            QMessageBox.critical(self, "Error Generate", f"Error: {str(e)}")
        finally:
            conn.close()

    # =========================
    # LOAD DATA LAPORAN
    # =========================
    def load_data(self):
        sel_year = self.comboBox.currentText()
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT k.nama_lengkap, k.jabatan, g.bulan,
                           g.gaji_pokok, g.total_tunjangan,
                           g.total_potongan, g.total_gaji, g.status_transfer
                    FROM gaji g
                    JOIN karyawan k ON g.karyawan_id=k.id
                    WHERE g.tahun=%s
                    ORDER BY g.bulan DESC
                """, (sel_year,))
                res = cur.fetchall()

                self.tableWidget.setRowCount(0)
                total = sent = pending = 0

                for r, d in enumerate(res):
                    self.tableWidget.insertRow(r)
                    for c, val in enumerate(d):
                        if isinstance(val, (int, float)):
                            self.tableWidget.setItem(r, c+1, QTableWidgetItem(f"{val:,.0f}"))
                        else:
                            self.tableWidget.setItem(r, c+1, QTableWidgetItem(str(val)))

                    self.tableWidget.setItem(r, 0, QTableWidgetItem(str(r+1)))

                    total += d[6]
                    if d[7] == 'Sudah Transfer':
                        sent += d[6]
                    else:
                        pending += d[6]

                self.lineEdit.setText(f"Rp {total:,.0f}")
                self.lineEdit_2.setText(f"Rp {sent:,.0f}")
                self.lineEdit_3.setText(f"Rp {pending:,.0f}")

            finally:
                conn.close()

    # =========================
    # EXPORT PDF
    # =========================
    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, 
            "Simpan PDF", 
            f"Laporan_Gaji_{self.comboBox.currentText()}.pdf", 
            "PDF Files (*.pdf)"
        )
        if not path:
            return
        
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    SELECT k.nama_lengkap, k.jabatan, g.bulan, g.total_gaji, g.status_transfer 
                    FROM gaji g 
                    JOIN karyawan k ON g.karyawan_id=k.id 
                    WHERE g.tahun=%s
                """, (self.comboBox.currentText(),))
                data = cur.fetchall()
                
                doc = SimpleDocTemplate(path, pagesize=landscape(letter))
                elements = []
                elements.append(Paragraph(f"<b>Laporan Gaji Tahun {self.comboBox.currentText()}</b>", getSampleStyleSheet()['Title']))
                elements.append(Spacer(1, 20))
                
                tbl_data = [['No', 'Nama', 'Jabatan', 'Bulan', 'Total Gaji', 'Status']]
                for idx, row in enumerate(data):
                    tbl_data.append([str(idx+1), row[0], row[1], str(row[2]), f"Rp {row[3]:,.0f}", row[4]])
                
                t = Table(tbl_data)
                t.setStyle(TableStyle([
                    ('GRID', (0,0), (-1,-1), 1, colors.black),
                    ('BACKGROUND', (0,0), (-1,0), colors.grey)
                ]))
                elements.append(t)
                doc.build(elements)
                QMessageBox.information(self, "Sukses", "PDF berhasil disimpan")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    # =========================
    # NAVIGATION
    # =========================
    def open_data_karyawan(self): self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_jabatan(self): self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_absensi(self): self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_validasi(self): self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()


# --- WINDOW: ABSENSI (UPDATED SESUAI UI BARU) ---
class AbsensiAdminWindow(QMainWindow, Ui_AbsensiWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)  # Memuat UI dari AbsensiAdmin.py
        self.previous_window = previous_window
        
        # 1. Setup Default Tanggal & Tampilan
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setDisplayFormat("MM/yyyy")
        self.pushButton.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold; border: 1px solid #ccc;")

        # 2. Setup Tabel & Data
        self.setup_tables()
        self.load_combo_karyawan()
        self.load_absensi()         
        self.load_notifikasi_cuti()
        
        # 3. Koneksi Navigasi
        self.pushButton_2.clicked.connect(self.back_to_dashboard)   
        self.pushButton_4.clicked.connect(self.open_data_karyawan)  
        self.pushButton_3.clicked.connect(self.open_jabatan)        
        self.pushButton_5.clicked.connect(self.open_laporan)        
        self.pushButton_6.clicked.connect(self.open_validasi)       
        self.pushButton_7.clicked.connect(self.open_arsip)          
        self.pushButton_8.clicked.connect(self.handle_logout)       
        
        # 4. Koneksi Fitur Absensi
        self.pushButton_9.clicked.connect(self.load_absensi)        
        self.pushButton_10.clicked.connect(self.approve_cuti)       
        self.pushButton_11.clicked.connect(self.reject_cuti)        

    def setup_tables(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_combo_karyawan(self):
        self.comboBox.clear()
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT nama_lengkap FROM karyawan WHERE status_akun='Aktif'")
                self.comboBox.addItem("Semua Karyawan")
                for r in cur.fetchall():
                    self.comboBox.addItem(r[0])
            except Exception as e: print(e)
            finally: conn.close()

    def load_absensi(self):
        bulan = self.dateEdit.date().month()
        tahun = self.dateEdit.date().year()
        filter_nama = self.comboBox.currentText()
        
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                sql = """
                    SELECT a.tanggal, k.nama_lengkap, k.jabatan, a.status 
                    FROM absensi a 
                    JOIN karyawan k ON a.karyawan_id = k.id 
                    WHERE MONTH(a.tanggal)=%s AND YEAR(a.tanggal)=%s
                """
                params = [bulan, tahun]
                if filter_nama != "Semua Karyawan":
                    sql += " AND k.nama_lengkap=%s"
                    params.append(filter_nama)
                sql += " ORDER BY a.tanggal DESC"
                
                cur.execute(sql, tuple(params))
                results = cur.fetchall()
                
                self.tableWidget.setRowCount(0)
                for row_idx, row_data in enumerate(results):
                    self.tableWidget.insertRow(row_idx)
                    self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
                    tgl = row_data[0].strftime("%d-%m-%Y") if row_data[0] else "-"
                    self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(tgl))
                    self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(row_data[1]))
                    self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(row_data[2]))
                    self.tableWidget.setItem(row_idx, 4, QTableWidgetItem(row_data[3]))
            except Exception as e: print(e)
            finally: conn.close()

    def load_notifikasi_cuti(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                sql = """SELECT c.id, k.nama_lengkap, c.tanggal_mulai, k.jabatan, c.status_validasi, c.jumlah_hari, c.alasan 
                         FROM cuti c JOIN karyawan k ON c.karyawan_id = k.id 
                         WHERE c.status_validasi='Pending'"""
                cur.execute(sql)
                results = cur.fetchall()
                
                self.tableWidget_2.setRowCount(0)
                for row_idx, row_data in enumerate(results):
                    self.tableWidget_2.insertRow(row_idx)
                    id_item = QTableWidgetItem(str(row_idx + 1))
                    id_item.setData(Qt.UserRole, row_data[0])
                    self.tableWidget_2.setItem(row_idx, 0, id_item)
                    self.tableWidget_2.setItem(row_idx, 1, QTableWidgetItem(row_data[1]))
                    tgl = row_data[2].strftime("%d-%m-%Y") if row_data[2] else "-"
                    self.tableWidget_2.setItem(row_idx, 2, QTableWidgetItem(tgl))
                    self.tableWidget_2.setItem(row_idx, 3, QTableWidgetItem(row_data[3]))
                    self.tableWidget_2.setItem(row_idx, 4, QTableWidgetItem(row_data[4]))
                    self.tableWidget_2.setItem(row_idx, 5, QTableWidgetItem(str(row_data[5])))
                    self.tableWidget_2.setItem(row_idx, 6, QTableWidgetItem(row_data[6]))
            except Exception as e: print(e)
            finally: conn.close()

    def approve_cuti(self): self.update_cuti_status("Disetujui")
    def reject_cuti(self): self.update_cuti_status("Ditolak")
    
    def update_cuti_status(self, status_baru):
        row = self.tableWidget_2.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Pilih data cuti dulu.")
            return
        cuti_id = self.tableWidget_2.item(row, 0).data(Qt.UserRole)
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE cuti SET status_validasi=%s WHERE id=%s", (status_baru, cuti_id))
                if status_baru == "Disetujui":
                    cur.execute("SELECT karyawan_id, tanggal_mulai, jumlah_hari FROM cuti WHERE id=%s", (cuti_id,))
                    res = cur.fetchone()
                    if res:
                        emp_id, start_date, duration = res
                        for i in range(duration):
                            curr_d = start_date + timedelta(days=i)
                            cur.execute("SELECT id FROM absensi WHERE karyawan_id=%s AND tanggal=%s", (emp_id, curr_d))
                            if not cur.fetchone():
                                cur.execute("INSERT INTO absensi (karyawan_id, tanggal, status) VALUES (%s, %s, 'Cuti')", (emp_id, curr_d))
                conn.commit()
                QMessageBox.information(self, "Sukses", f"Status: {status_baru}")
                self.load_notifikasi_cuti()
                self.load_absensi()
            except Exception as e: QMessageBox.critical(self, "Error", str(e))
            finally: conn.close()

    def open_data_karyawan(self): self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_jabatan(self): self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_laporan(self): self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_validasi(self): self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()

# --- WINDOW: JABATAN (LOGIKA SIMPAN & FORMAT UANG FIXED) ---
class JabatanWindow(BaseWindow, Ui_JabatanWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        self.setup_table()
        self.pushButton_3.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.pushButton_9.clicked.connect(self.handle_add)
        self.pushButton_11.clicked.connect(self.handle_edit)
        self.pushButton_10.clicked.connect(self.handle_delete)
        QTimer.singleShot(100, self.load_data)

    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran FROM jabatan")
                res = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for r, d in enumerate(res):
                    self.tableWidget.insertRow(r)
                    it = QTableWidgetItem(str(r+1))
                    it.setData(Qt.UserRole, d[0])
                    self.tableWidget.setItem(r,0,it)
                    self.tableWidget.setItem(r,1,QTableWidgetItem(d[1]))
                    # Format Rupiah: 4,000,000
                    self.tableWidget.setItem(r,2,QTableWidgetItem(f"{d[2]:,.0f}"))
                    self.tableWidget.setItem(r,3,QTableWidgetItem(f"{d[3]:,.0f}"))
                    self.tableWidget.setItem(r,4,QTableWidgetItem(f"{d[4]:,.0f}"))
            finally: conn.close()

    def handle_add(self):
        d = JabatanDialog(self)
        if d.exec() == QDialog.Accepted:
            dat = d.get_data()
            
            # 1. Validasi Nama tidak boleh kosong
            if not dat['nama']:
                QMessageBox.warning(self, "Peringatan", "Nama Jabatan wajib diisi!")
                return

            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    # 2. Hapus Try-Except kosong agar ketahuan jika ada error (misal duplikat)
                    cursor.execute("INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran) VALUES (%s,%s,%s,%s)", (dat['nama'], dat['gaji'], dat['tunj_jab'], dat['tunj_hadir']))
                    conn.commit()
                    self.load_data()
                    QMessageBox.information(self, "Sukses", "Jabatan berhasil ditambahkan!")
                except mysql.connector.Error as err:
                    QMessageBox.critical(self, "Gagal Menyimpan", f"Error: {err}")
                finally: conn.close()

    def handle_edit(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        idj = self.tableWidget.item(r,0).data(Qt.UserRole)
        
        # Bersihkan format ribuan (koma) agar bisa masuk ke SpinBox
        def clean_money(text):
            return text.replace(",", "").replace("Rp", "").strip()

        old = {
            'nama': self.tableWidget.item(r,1).text(), 
            'gaji': clean_money(self.tableWidget.item(r,2).text()), 
            'tunj_jab': clean_money(self.tableWidget.item(r,3).text()), 
            'tunj_hadir': clean_money(self.tableWidget.item(r,4).text())
        }
        
        d = JabatanDialog(self, old)
        if d.exec() == QDialog.Accepted:
            dat = d.get_data()
            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    cursor.execute("UPDATE jabatan SET nama_jabatan=%s, gaji_pokok=%s, tunjangan_jabatan=%s, tunjangan_kehadiran=%s WHERE id=%s", (dat['nama'], dat['gaji'], dat['tunj_jab'], dat['tunj_hadir'], idj))
                    conn.commit()
                    self.load_data()
                    QMessageBox.information(self, "Sukses", "Data jabatan diperbarui!")
                except mysql.connector.Error as err:
                    QMessageBox.critical(self, "Error", f"Gagal update: {err}")
                finally: conn.close()

    def handle_delete(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        if QMessageBox.question(self, "Hapus", "Yakin?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM jabatan WHERE id=%s", (self.tableWidget.item(r,0).data(Qt.UserRole),))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

# --- WINDOW: DATA KARYAWAN ---
class DataKaryawanWindow(BaseWindow, Ui_DataKaryawanWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        self.setup_table_behavior()
        self.pushButton_4.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        
        self.pushButton_9.clicked.connect(self.open_add_employee)
        self.pushButton_11.clicked.connect(self.handle_edit)
        self.pushButton_10.clicked.connect(self.handle_delete)
        
        QTimer.singleShot(100, self.load_data)

    def setup_table_behavior(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nama_lengkap, jabatan, status_kerja, tanggal_gabung, status_akun FROM karyawan WHERE status_akun='Aktif'")
                res = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for r, d in enumerate(res):
                    self.tableWidget.insertRow(r)
                    it = QTableWidgetItem(str(r+1))
                    it.setData(Qt.UserRole, d[0])
                    self.tableWidget.setItem(r,0,it)
                    self.tableWidget.setItem(r,1,QTableWidgetItem(str(d[1])))
                    self.tableWidget.setItem(r,2,QTableWidgetItem(str(d[2])))
                    self.tableWidget.setItem(r,3,QTableWidgetItem(str(d[3])))
                    self.tableWidget.setItem(r,4,QTableWidgetItem(str(d[4])))
                    self.tableWidget.setItem(r,5,QTableWidgetItem(str(d[5])))
            finally: conn.close()

    def open_add_employee(self):
        d = AddEmployeeDialog(self)
        if d.exec() == QDialog.Accepted:
            data = d.get_data()
            if not all([data['nama'], data['email'], data['password']]):
                QMessageBox.warning(self, "Peringatan", "Nama, Email, dan Password harus diisi!")
                return
            
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM karyawan WHERE email=%s", (data['email'],))
                    if cursor.fetchone():
                        QMessageBox.warning(self, "Gagal", "Email sudah terdaftar!")
                        return
                    
                    sql = "INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES (%s, %s, %s, %s, %s, 'Aktif', %s)"
                    val = (data['nama'], data['email'], data['password'], data['jabatan'], data['status_kerja'], date.today())
                    cursor.execute(sql, val)
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Karyawan berhasil ditambahkan!")
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))
                finally:
                    conn.close()

    def handle_edit(self):
        r = self.tableWidget.currentRow()
        if r < 0:
            QMessageBox.warning(self, "Info", "Pilih Baris yang ingin diedit")
            return
        idk = self.tableWidget.item(r,0).data(Qt.UserRole)
        curr = {'nama': self.tableWidget.item(r,1).text(), 'jabatan': self.tableWidget.item(r,2).text(), 'status_kerja': self.tableWidget.item(r,3).text(), 'status_akun': self.tableWidget.item(r,5).text()}
        d = EditEmployeeDialog(self, curr)
        if d.exec() == QDialog.Accepted:
            new = d.get_updated_data()
            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    cursor.execute("UPDATE karyawan SET nama_lengkap=%s, jabatan=%s, status_kerja=%s, status_akun=%s WHERE id=%s", (new['nama'], new['jabatan'], new['status_kerja'], new['status_akun'], idk))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def handle_delete(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        idk = self.tableWidget.item(r,0).data(Qt.UserRole)
        nama = self.tableWidget.item(r,1).text()
        if QMessageBox.question(self, "Hapus", f"Yakin ingin menonaktifkan '{nama}'? Data akan pindah ke Arsip.", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    cursor.execute("UPDATE karyawan SET status_akun='Nonaktif' WHERE id=%s", (idk,))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

# --- DASHBOARD ADMIN ---
class AdminDashboard(QMainWindow, Ui_AdminWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data_karyawan_window = None
        self.jabatan_window = None
        self.absensi_window = None
        self.laporan_window = None
        self.validasi_window = None
        self.arsip_window = None
        
        self.pushButton_2.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.pushButton_8.clicked.connect(self.handle_logout)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_7.clicked.connect(self.open_arsip)
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.load_dashboard_data()

    def load_dashboard_data(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM karyawan WHERE status_akun = 'Aktif'")
                self.label_5.setText(str(cur.fetchone()[0]))
                cur.execute("SELECT COUNT(*) FROM karyawan WHERE status_akun = 'Nonaktif'")
                self.label_7.setText(str(cur.fetchone()[0]))
                cur.execute("SELECT nama_lengkap, jabatan, status_kerja, tanggal_gabung FROM karyawan WHERE status_akun='Aktif' LIMIT 5")
                res = cur.fetchall()
                self.tableWidget.setRowCount(0)
                for r, row in enumerate(res):
                    self.tableWidget.insertRow(r)
                    self.tableWidget.setItem(r,0,QTableWidgetItem(str(r+1)))
                    for c, d in enumerate(row):
                        self.tableWidget.setItem(r,c+1,QTableWidgetItem(str(d)))
            finally: conn.close()

    def open_data_karyawan(self):
        if not self.data_karyawan_window: self.data_karyawan_window = DataKaryawanWindow(self)
        self.data_karyawan_window.load_data(); self.hide(); self.data_karyawan_window.show()
    def open_jabatan(self):
        if not self.jabatan_window: self.jabatan_window = JabatanWindow(self)
        self.jabatan_window.load_data(); self.hide(); self.jabatan_window.show()
    def open_absensi(self):
        if not self.absensi_window: self.absensi_window = AbsensiAdminWindow(self)
        self.absensi_window.load_absensi(); self.hide(); self.absensi_window.show()
    def open_laporan(self):
        if not self.laporan_window: self.laporan_window = LaporanGajiWindow(self)
        self.laporan_window.load_data(); self.hide(); self.laporan_window.show()
    def open_validasi(self):
        if not self.validasi_window: self.validasi_window = ValidasiGajiWindow(self)
        self.validasi_window.load_data(); self.hide(); self.validasi_window.show()
    def open_arsip(self):
        if not self.arsip_window: self.arsip_window = ArsipNonaktifWindow(self)
        self.arsip_window.load_data(); self.hide(); self.arsip_window.show()
    def handle_logout(self): self.close(); global window; window.show()

# --- EMPLOYEE DASHBOARD ---
class EmployeeDashboard(QMainWindow, Ui_AbsensiKaryawanWindow):
    def __init__(self, user_data):
        super().__init__()
        self.setupUi(self)
        self.user = user_data

        self.label_15.setText(f"Sistem Manajemen Karyawan Toko Roti - {self.user['nama']}")
        self.pushButton_2.setStyleSheet(
            "background-color: #d6dc82; color: #262628; font-weight: bold;"
        )

        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_3.setSelectionMode(QAbstractItemView.SingleSelection)

        self.load_absensi_history()

        self.pushButton_14.clicked.connect(self.absen_datang)
        self.pushButton_6.clicked.connect(self.absen_pulang)
        self.pushButton_4.clicked.connect(self.open_slip_gaji)
        self.pushButton.clicked.connect(self.open_riwayat_cuti)
        self.pushButton_5.clicked.connect(self.open_pengajuan_cuti)
        self.pushButton_8.clicked.connect(self.handle_logout)

    # ================= NAVIGASI (FIX) =================

    def open_slip_gaji(self):
        self.slip_window = SlipGajiWindow(self.user, previous_window=self)
        self.slip_window.load_slip()
        self.slip_window.show()
        self.close()

    def open_riwayat_cuti(self):
        self.riwayat_window = RiwayatCutiWindow(self.user, previous_window=self)
        self.riwayat_window.load_data()
        self.riwayat_window.show()
        self.close()

    def open_pengajuan_cuti(self):
        self.pengajuan_window = PengajuanCutiWindow(self.user, previous_window=self)
        self.pengajuan_window.show()
        self.close()

    # ================= LOGIC TETAP =================

    def load_absensi_history(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT tanggal, waktu_masuk, waktu_pulang, status "
                    "FROM absensi WHERE karyawan_id=%s "
                    "ORDER BY tanggal DESC LIMIT 200",
                    (self.user['id'],)
                )
                self.tableWidget_3.setRowCount(0)
                for r, row in enumerate(cur.fetchall()):
                    self.tableWidget_3.insertRow(r)
                    self.tableWidget_3.setItem(r, 0, QTableWidgetItem(str(r+1)))
                    self.tableWidget_3.setItem(
                        r, 1,
                        QTableWidgetItem(row[0].strftime("%d-%m-%Y") if row[0] else "-")
                    )
                    self.tableWidget_3.setItem(r, 2, QTableWidgetItem(str(row[1]) if row[1] else "-"))
                    self.tableWidget_3.setItem(r, 3, QTableWidgetItem(str(row[2]) if row[2] else "-"))
                    self.tableWidget_3.setItem(r, 4, QTableWidgetItem(str(row[3]) if row[3] else "-"))
            finally:
                conn.close()

    def absen_datang(self):
        today = date.today()
        now = datetime.now().strftime("%H:%M:%S")
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, waktu_masuk FROM absensi "
                    "WHERE karyawan_id=%s AND tanggal=%s",
                    (self.user['id'], today)
                )
                row = cur.fetchone()
                if row and row[1]:
                    QMessageBox.information(self, "Info", "Anda sudah absen datang hari ini.")
                elif row:
                    cur.execute(
                        "UPDATE absensi SET waktu_masuk=%s, status='Hadir' WHERE id=%s",
                        (now, row[0])
                    )
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Absen datang tercatat.")
                else:
                    cur.execute(
                        "INSERT INTO absensi (karyawan_id, tanggal, waktu_masuk, status) "
                        "VALUES (%s,%s,%s,'Hadir')",
                        (self.user['id'], today, now)
                    )
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Absen datang tercatat.")
                self.load_absensi_history()
            finally:
                conn.close()

    def absen_pulang(self):
        today = date.today()
        now = datetime.now().strftime("%H:%M:%S")
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, waktu_pulang FROM absensi "
                    "WHERE karyawan_id=%s AND tanggal=%s",
                    (self.user['id'], today)
                )
                row = cur.fetchone()
                if row and row[1]:
                    QMessageBox.information(self, "Info", "Anda sudah absen pulang hari ini.")
                elif row:
                    cur.execute(
                        "UPDATE absensi SET waktu_pulang=%s WHERE id=%s",
                        (now, row[0])
                    )
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Absen pulang tercatat.")
                else:
                    QMessageBox.warning(self, "Warning", "Silakan absen datang terlebih dahulu.")
                self.load_absensi_history()
            finally:
                conn.close()

    def handle_logout(self):
        self.close()
        global window
        window.show()

# --- SLIP GAJI WINDOW ---

class SlipGajiWindow(QMainWindow, Ui_SlipGajiWindow):
    def __init__(self, user, previous_window):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.previous_window = previous_window
        self.current_gaji_id = None
        self.current_bulan = None
        self.current_tahun = None
        
        # Setup navigasi buttons
        self.pushButton_8.clicked.connect(self.back)
        if hasattr(self, 'pushButton'): self.pushButton.clicked.connect(self.open_riwayat_cuti)
        if hasattr(self, 'pushButton_5'): self.pushButton_5.clicked.connect(self.open_pengajuan_cuti)
        # Hapus button tutup
        if hasattr(self, 'pushButton_2'): 
            try: self.pushButton_2.hide()
            except: pass
        
        # Setup lineEdit sebagai read-only
        self.setup_readonly_fields()
        
        # Resize font pada label untuk keterbacaan
        self.setup_label_fonts()
        
        # Setup button labels dan connections
        if hasattr(self, 'pushButton_10'): 
            self.pushButton_10.setText("Cetak Slip")
            self.pushButton_10.clicked.connect(self.export_pdf_slip)
        if hasattr(self, 'pushButton_11'): 
            self.pushButton_11.setText("Validasi")
            self.pushButton_11.clicked.connect(self.validasi_slip)
        if hasattr(self, 'pushButton_12'): 
            self.pushButton_12.hide()
    
    def setup_readonly_fields(self):
        """Setup lineEdit sebagai field read-only dengan styling seperti label"""
        readonly_fields = [self.lineEdit, self.lineEdit_2, self.lineEdit_3, 
                          self.lineEdit_4, self.lineEdit_5, self.lineEdit_6,
                          self.lineEdit_7, self.lineEdit_8]
        for field in readonly_fields:
            field.setReadOnly(True)
            field.setFocusPolicy(Qt.NoFocus)
            field.setStyleSheet("""
                QLineEdit {
                    background-color: #f9f9f9;
                    color: #262628;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    padding: 4px;
                    font-size: 7pt;
                    font-weight: 500;
                }
            """)

    def setup_label_fonts(self):
        """Resize font pada semua label agar terbaca"""
        try:
            font = self.font()
            font.setPointSize(9)
            for widget in self.findChildren(QLabel):
                widget.setFont(font)
        except:
            pass

    def load_slip(self):
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, bulan, tahun, gaji_pokok, total_tunjangan, total_potongan, total_gaji, status_transfer, status_validasi "
                "FROM gaji WHERE karyawan_id=%s "
                "ORDER BY tahun DESC, bulan DESC LIMIT 1",
                (self.user['id'],)
            )
            row = cur.fetchone()
            conn.close()
            if row:
                gaji_id, bulan, tahun, pokok, tunj, potong, total, status_transfer, status_validasi = row
                self.current_gaji_id = gaji_id
                self.current_bulan = bulan
                self.current_tahun = tahun
                
                bulan_names = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                              "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                bulan_text = bulan_names[bulan] if 1 <= bulan <= 12 else str(bulan)
                
                # Hitung bonus: 5% jika sudah divalidasi
                bonus = total * 0.05 if status_validasi == 'Valid' else 0
                total_bersih = total + bonus
                
                self.lineEdit.setText(f"{bulan_text} {tahun}")
                self.lineEdit_2.setText(f"{status_validasi}")
                self.lineEdit_3.setText(f"Rp {pokok:,.0f}")
                self.lineEdit_4.setText(f"Rp {tunj:,.0f}")
                self.lineEdit_5.setText(f"Rp {potong:,.0f}")
                self.lineEdit_6.setText(f"Rp {bonus:,.0f}")
                self.lineEdit_7.setText(f"Rp {total:,.0f}")
                self.lineEdit_8.setText(f"Rp {total_bersih:,.0f}")
                
                if hasattr(self, 'pushButton_11'):
                    self.pushButton_11.setEnabled(status_validasi == 'Pending')
                    if status_validasi == 'Valid':
                        self.pushButton_11.setText("✓ Sudah Divalidasi")
                        self.pushButton_11.setStyleSheet("""
                            QPushButton {
                                background-color: #90EE90;
                                color: #262628;
                                font-weight: bold;
                                padding: 5px;
                                border-radius: 3px;
                            }
                        """)
            else:
                self.current_gaji_id = None
                self.lineEdit.setText("Belum ada slip gaji")
                self.lineEdit_2.setText("---")
                self.lineEdit_3.setText("Rp 0")
                self.lineEdit_4.setText("Rp 0")
                self.lineEdit_5.setText("Rp 0")
                self.lineEdit_6.setText("Rp 0")
                self.lineEdit_7.setText("Rp 0")
                self.lineEdit_8.setText("Rp 0")
                if hasattr(self, 'pushButton_11'):
                    self.pushButton_11.setEnabled(False)

    def export_pdf_slip(self):
        """Generate dan export slip gaji ke PDF"""
        if not self.current_gaji_id:
            QMessageBox.warning(self, "Info", "Belum ada data slip gaji untuk dicetak")
            return
        
        try:
            conn = create_connection()
            if not conn:
                QMessageBox.critical(self, "Error", "Koneksi database gagal")
                return
            
            cur = conn.cursor()
            cur.execute("""
                SELECT g.bulan, g.tahun, g.gaji_pokok, g.total_tunjangan, 
                       g.total_potongan, g.total_gaji, g.status_validasi,
                       k.nama_lengkap, k.jabatan
                FROM gaji g
                JOIN karyawan k ON g.karyawan_id = k.id
                WHERE g.id=%s
            """, (self.current_gaji_id,))
            data = cur.fetchone()
            conn.close()
            
            if not data:
                QMessageBox.warning(self, "Error", "Data slip gaji tidak ditemukan")
                return
            
            bulan_num, tahun, pokok, tunj, potong, total, status_validasi, nama, jabatan = data
            bonus = total * 0.05 if status_validasi == 'Valid' else 0
            total_bersih = total + bonus
            
            bulan_names = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                          "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            bulan_text = bulan_names[bulan_num] if 1 <= bulan_num <= 12 else str(bulan_num)
            
            path, _ = QFileDialog.getSaveFileName(
                self,
                "Simpan Slip Gaji",
                f"Slip_Gaji_{nama}_{bulan_num}_{tahun}.pdf",
                "PDF Files (*.pdf)"
            )
            if not path:
                return
            
            doc = SimpleDocTemplate(path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            elements.append(Paragraph("<b>SLIP GAJI KARYAWAN</b>", styles['Title']))
            elements.append(Paragraph("<b>PT. Toko Roti Indonesia</b>", styles['Normal']))
            elements.append(Spacer(1, 12))
            
            info_data = [
                ["Nama Karyawan:", nama],
                ["Jabatan:", jabatan],
                ["Periode Gaji:", f"{bulan_text} {tahun}"],
                ["Status:", status_validasi],
            ]
            info_table = Table(info_data, colWidths=[150, 350])
            info_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#f0f0f0'), colors.white])
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 20))
            
            gaji_data = [
                ["Keterangan", "Jumlah"],
                ["Gaji Pokok", f"Rp {pokok:,.0f}"],
                ["Tunjangan", f"Rp {tunj:,.0f}"],
                ["Potongan", f"Rp {potong:,.0f}"],
                ["Bonus (5%)", f"Rp {bonus:,.0f}"],
                ["TOTAL GAJI BERSIH", f"Rp {total_bersih:,.0f}"],
            ]
            gaji_table = Table(gaji_data, colWidths=[300, 200])
            gaji_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d6dc82')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#90EE90')),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9f9f9')])
            ]))
            elements.append(gaji_table)
            elements.append(Spacer(1, 30))
            
            elements.append(Paragraph(f"<i>Tanggal Terbit: {date.today().strftime('%d-%m-%Y')}</i>", styles['Normal']))
            elements.append(Paragraph(f"<i>Diterbitkan oleh: Sistem Manajemen Gaji</i>", styles['Normal']))
            
            doc.build(elements)
            QMessageBox.information(self, "Sukses", "Slip gaji berhasil disimpan!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal membuat PDF: {str(e)}")

    def validasi_slip(self):
        """Validasi slip gaji - update status_validasi menjadi 'Valid'"""
        if not self.current_gaji_id:
            QMessageBox.warning(self, "Info", "Tidak ada slip gaji untuk divalidasi")
            return
        
        if QMessageBox.question(
            self,
            "Konfirmasi Validasi",
            "Validasi slip gaji ini?\nStatus akan berubah menjadi 'Valid' dan Anda mendapat bonus 5%.",
            QMessageBox.Yes | QMessageBox.No
        ) != QMessageBox.Yes:
            return
        
        try:
            conn = create_connection()
            if not conn:
                QMessageBox.critical(self, "Error", "Koneksi database gagal")
                return
            
            cur = conn.cursor()
            cur.execute(
                "UPDATE gaji SET status_validasi='Valid' WHERE id=%s",
                (self.current_gaji_id,)
            )
            conn.commit()
            conn.close()
            
            QMessageBox.information(
                self, "Sukses", 
                "Slip gaji telah divalidasi!\n"
                "Status berubah menjadi 'Valid'\n"
                "Bonus 5% akan ditambahkan ke total gaji bersih."
            )
            
            self.load_slip()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Validasi gagal: {str(e)}")

    def open_riwayat_cuti(self):
        self.riwayat_window = RiwayatCutiWindow(self.user, previous_window=self.previous_window)
        self.riwayat_window.load_data()
        self.riwayat_window.show()
        self.close()

    def open_pengajuan_cuti(self):
        self.pengajuan_window = PengajuanCutiWindow(self.user, previous_window=self.previous_window)
        self.pengajuan_window.show()
        self.close()

    def back(self):
        self.previous_window.show()
        self.close()

# --- RIWAYAT CUTI WINDOW ---

class RiwayatCutiWindow(QMainWindow, Ui_RiwayatCutiWindow):
    def __init__(self, user, previous_window):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.previous_window = previous_window
        
        # Setup navigasi buttons
        self.pushButton_8.clicked.connect(self.back)
        if hasattr(self, 'pushButton_4'): self.pushButton_4.clicked.connect(self.open_slip_gaji)
        if hasattr(self, 'pushButton_5'): self.pushButton_5.clicked.connect(self.open_pengajuan_cuti)
        if hasattr(self, 'pushButton_2'): self.pushButton_2.clicked.connect(self.back)

    def load_data(self):
        self.tableWidget_3.setRowCount(0)
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT tanggal_mulai, jumlah_hari, alasan, status_validasi "
                "FROM cuti WHERE karyawan_id=%s "
                "ORDER BY tanggal_mulai DESC",
                (self.user['id'],)
            )
            for r, d in enumerate(cur.fetchall()):
                self.tableWidget_3.insertRow(r)
                self.tableWidget_3.setItem(r,0,QTableWidgetItem(str(r+1)))
                self.tableWidget_3.setItem(r,1,QTableWidgetItem(d[0].strftime("%d-%m-%Y")))
                self.tableWidget_3.setItem(r,2,QTableWidgetItem(self.user['nama']))
                self.tableWidget_3.setItem(r,3,QTableWidgetItem(str(d[1])))
                self.tableWidget_3.setItem(r,4,QTableWidgetItem(d[2]))
                self.tableWidget_3.setItem(r,5,QTableWidgetItem(d[3]))
            conn.close()

    def open_slip_gaji(self):
        self.slip_window = SlipGajiWindow(self.user, previous_window=self.previous_window)
        self.slip_window.load_slip()
        self.slip_window.show()
        self.close()

    def open_pengajuan_cuti(self):
        self.pengajuan_window = PengajuanCutiWindow(self.user, previous_window=self.previous_window)
        self.pengajuan_window.show()
        self.close()

    def back(self):
        self.previous_window.show()
        self.close()

# --- PENGAJUAN CUTI WINDOW ---
class PengajuanCutiWindow(QMainWindow, Ui_PengajuanCutiWindow):
    def __init__(self, user, previous_window):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.previous_window = previous_window

        self.lineEdit.setText(self.user['nama'])
        self.lineEdit_2.setText(self.user['jabatan'])

        # Setup navigasi buttons
        self.pushButton_12.clicked.connect(self.send_pengajuan)
        self.pushButton_8.clicked.connect(self.back)
        if hasattr(self, 'pushButton_4'): self.pushButton_4.clicked.connect(self.open_slip_gaji)
        if hasattr(self, 'pushButton'): self.pushButton.clicked.connect(self.open_riwayat_cuti)
        if hasattr(self, 'pushButton_2'): self.pushButton_2.clicked.connect(self.back)

    def send_pengajuan(self):
        bulan = self.comboBox_2.currentIndex() + 1
        tahun = int(self.comboBox.currentText())
        jumlah = self.lineEdit_3.text()
        alasan = self.lineEdit_4.text()

        if not jumlah or not alasan:
            QMessageBox.warning(self, "Info", "Lengkapi data.")
            return

        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO cuti (karyawan_id, tanggal_mulai, jumlah_hari, alasan) "
                "VALUES (%s,%s,%s,%s)",
                (self.user['id'], date(tahun, bulan, 1), int(jumlah), alasan)
            )
            conn.commit()
            conn.close()

        QMessageBox.information(self, "Sukses", "Pengajuan cuti dikirim.")
        self.back()

    def open_slip_gaji(self):
        self.slip_window = SlipGajiWindow(self.user, previous_window=self.previous_window)
        self.slip_window.load_slip()
        self.slip_window.show()
        self.close()

    def open_riwayat_cuti(self):
        self.riwayat_window = RiwayatCutiWindow(self.user, previous_window=self.previous_window)
        self.riwayat_window.load_data()
        self.riwayat_window.show()
        self.close()

    def back(self):
        self.previous_window.show()
        self.close()

# --- REGISTER & LOGIN ---
class RegisterWindow(QMainWindow, Ui_RegisterWindow):
    def __init__(self, login_window):
        super().__init__()
        self.setupUi(self)
        self.login_window = login_window
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Password)
        self.pushButton.clicked.connect(self.handle_register)
        self.label_4.setCursor(Qt.PointingHandCursor)
        self.label_4.mousePressEvent = lambda e: (self.hide(), self.login_window.show())

    def handle_register(self):
        n, e, p, cp = self.lineEdit_3.text(), self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_4.text()
        if not all([n,e,p,cp]):
            QMessageBox.warning(self, "Info", "Isi semua field.")
            return
        if p != cp:
            QMessageBox.warning(self, "Info", "Password tidak cocok.")
            return
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id FROM karyawan WHERE email=%s", (e,))
                if cur.fetchone():
                    QMessageBox.warning(self, "Gagal", "Email sudah terdaftar.")
                    return
                # Default role: Baker, Kontrak
                cur.execute("INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES (%s,%s,%s,'Baker','Kontrak','Aktif',%s)", (n,e,p,date.today()))
                conn.commit()
                QMessageBox.information(self, "Sukses", "Registrasi Berhasil! Silakan Login.")
                self.hide()
                self.login_window.show()
            finally: conn.close()

class LoginWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.reg_win = None
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.pushButton.clicked.connect(self.handle_login)
        self.label_4.setCursor(Qt.PointingHandCursor)
        self.label_4.mousePressEvent = self.open_reg

    def open_reg(self, e): 
        if not self.reg_win: self.reg_win = RegisterWindow(self)
        self.hide()
        self.reg_win.show()

    def handle_login(self):
        e, p = self.lineEdit.text(), self.lineEdit_2.text()
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, nama_lengkap, jabatan, status_akun FROM karyawan WHERE email=%s AND password=%s", (e,p))
                user = cur.fetchone()
                if user:
                    if user[3] != 'Aktif':
                        QMessageBox.critical(self, "Gagal", "Akun Anda Nonaktif. Hubungi Admin.")
                        return
                    self.hide()
                    if user[2].lower() == 'admin':
                        self.dash = AdminDashboard()
                    else:
                        self.dash = EmployeeDashboard({'id': user[0], 'nama': user[1], 'jabatan': user[2]})
                    self.dash.show()
                else:
                    QMessageBox.warning(self, "Gagal", "Email atau Password Salah.")
            finally: conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_all_tables() 
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())