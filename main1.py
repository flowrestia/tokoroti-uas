import sys
import mysql.connector
from datetime import date, datetime, timedelta

# --- IMPORT LIBRARY UI ---
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel,
                               QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt, QDate, QTimer, QLocale

# --- LIBRARY PDF ---
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# --- IMPORT FILE UI ---
from Login import Ui_MainWindow as Ui_LoginWindow
from DashboardAdmin import Ui_MainWindow as Ui_AdminWindow
from Register import Ui_MainWindow as Ui_RegisterWindow
from DataKaryawan import Ui_MainWindow as Ui_DataKaryawanWindow
from Jabatan import Ui_MainWindow as Ui_JabatanWindow
from AbsensiAdmin import Ui_MainWindow as Ui_AbsensiWindow
from LaporanGaji import Ui_MainWindow as Ui_LaporanGajiWindow
from ValidasiGaji import Ui_MainWindow as Ui_ValidasiGajiWindow
from ArsipNonaktif import Ui_MainWindow as Ui_ArsipNonaktifWindow

# --- KONEKSI DATABASE ---
def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost", 
            user="root", 
            password="", 
            database="bakery_management"
        )
    except mysql.connector.Error:
        return None

# --- INISIALISASI DATABASE ---
def init_all_tables():
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Tabel Jabatan
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jabatan (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nama_jabatan VARCHAR(50) NOT NULL UNIQUE,
                    gaji_pokok DOUBLE NOT NULL,
                    tunjangan_jabatan DOUBLE NOT NULL,
                    tunjangan_kehadiran DOUBLE NOT NULL
                )
            """)
            # Tabel Karyawan
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
            # Tabel Absensi, Cuti, Gaji
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
                    tanggal_transfer DATE,
                    bukti_transfer VARCHAR(255),
                    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE CASCADE
                )
            """)
            
            # Data Dummy
            cursor.execute("SELECT COUNT(*) FROM jabatan")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran) VALUES ('Admin', 4000000, 500000, 200000), ('Kasir', 3000000, 250000, 150000), ('Baker', 3500000, 300000, 150000)")
            cursor.execute("SELECT COUNT(*) FROM karyawan")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES ('Super Admin', 'admin@toko.com', 'admin123', 'Admin', 'Tetap', 'Aktif', %s)", (date.today(),))
            conn.commit()
        except Exception as e:
            print(f"Database Init Error: {e}")
        finally:
            conn.close()

# --- DIALOG BARU: TAMBAH KARYAWAN ---
class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Karyawan Baru")
        self.resize(400, 350)
        
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.input_nama = QLineEdit(self)
        self.input_nama.setPlaceholderText("Nama Lengkap")
        
        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Email Login")
        
        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.combo_jabatan = QComboBox(self)
        self.load_jabatan_combo()

        self.combo_status_kerja = QComboBox(self)
        self.combo_status_kerja.addItems(["Tetap", "Kontrak", "Magang"])

        form.addRow("Nama Lengkap:", self.input_nama)
        form.addRow("Email:", self.input_email)
        form.addRow("Password:", self.input_password)
        form.addRow("Jabatan:", self.combo_jabatan)
        form.addRow("Status Kerja:", self.combo_status_kerja)

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
            'status_kerja': self.combo_status_kerja.currentText()
        }

# --- DIALOG: EDIT KARYAWAN ---
class EditEmployeeDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Data Karyawan")
        self.resize(400, 300)
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
        self.combo_status_kerja.addItems(["Tetap", "Kontrak", "Magang"])
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

# --- DIALOG: JABATAN (LOGIKA INPUT UANG DIPERBAIKI) ---
class JabatanDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setWindowTitle("Form Jabatan")
        self.resize(400, 300)
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        self.input_nama = QLineEdit(self)
        self.input_nama.setPlaceholderText("Contoh: Manager")
        
        # Pengaturan Input Gaji (Tanpa Desimal, Limit Besar)
        self.input_gaji = QDoubleSpinBox(self)
        self.setup_currency_input(self.input_gaji)

        self.input_tunj_jab = QDoubleSpinBox(self)
        self.setup_currency_input(self.input_tunj_jab)
        
        self.input_tunj_hadir = QDoubleSpinBox(self)
        self.setup_currency_input(self.input_tunj_hadir)
        
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

    def setup_currency_input(self, spinbox):
        # Setting agar tampilan seperti rupiah (100.000) tanpa .00
        spinbox.setDecimals(0) # Hilangkan desimal
        spinbox.setRange(0, 9999999999) # Limit hingga 9 Milyar
        spinbox.setGroupSeparatorShown(True) # Tampilkan titik pemisah ribuan
        spinbox.setSingleStep(100000) # Sekali klik naik 100rb
        # Tambahkan prefix Rp (Opsional, kadang bikin error tampilan di beberapa OS, aman dihilangkan)
        # spinbox.setPrefix("Rp ") 

    def get_data(self):
        return {
            'nama': self.input_nama.text(),
            'gaji': self.input_gaji.value(),
            'tunj_jab': self.input_tunj_jab.value(),
            'tunj_hadir': self.input_tunj_hadir.value()
        }

# --- BASE WINDOW ---
class BaseWindow(QMainWindow):
    def __init__(self, previous_window):
        super().__init__()
        self.previous_window = previous_window

    def setup_nav(self):
        try: self.pushButton_2.clicked.connect(self.back_to_dashboard)
        except: pass
        try: self.pushButton_4.clicked.connect(self.open_data_karyawan)
        except: pass
        try: self.pushButton_3.clicked.connect(self.open_jabatan)
        except: pass
        try: self.pushButton.clicked.connect(self.open_absensi)
        except: pass
        try: self.pushButton_5.clicked.connect(self.open_laporan)
        except: pass
        try: self.pushButton_6.clicked.connect(self.open_validasi)
        except: pass
        try: self.pushButton_7.clicked.connect(self.open_arsip)
        except: pass
        try: self.pushButton_8.clicked.connect(self.handle_logout)
        except: pass

    def open_data_karyawan(self): self._open_win(DataKaryawanWindow)
    def open_jabatan(self): self._open_win(JabatanWindow)
    def open_absensi(self): self._open_win(AbsensiAdminWindow)
    def open_laporan(self): self._open_win(LaporanGajiWindow)
    def open_validasi(self): self._open_win(ValidasiGajiWindow)
    def open_arsip(self): self._open_win(ArsipNonaktifWindow)
    
    def _open_win(self, WindowClass):
        self.hide()
        QTimer.singleShot(10, lambda: self._show_new_window(WindowClass))

    def _show_new_window(self, WindowClass):
        self.win = WindowClass(self.previous_window)
        self.win.show()

    def back_to_dashboard(self):
        if self.previous_window is None:
            return 
        self.hide()
        self.previous_window.load_dashboard_data()
        self.previous_window.show()

    def handle_logout(self):
        self.close()
        global window
        window.show()

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

# --- WINDOW LAINNYA ---
class ArsipNonaktifWindow(BaseWindow, Ui_ArsipNonaktifWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        self.pushButton_7.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.pushButton_11.setText("Pulihkan (Aktifkan)")
        self.pushButton_10.setText("Hapus Permanen")
        self.setup_table()
        
        self.pushButton_11.clicked.connect(self.restore_employee)
        self.pushButton_10.clicked.connect(self.delete_permanent)
        
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
        if row < 0: return
        emp_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        nama = self.tableWidget.item(row, 1).text()
        if QMessageBox.question(self, "Konfirmasi", f"Aktifkan kembali '{nama}'?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE karyawan SET status_akun='Aktif' WHERE id=%s", (emp_id,))
                    conn.commit()
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

class ValidasiGajiWindow(BaseWindow, Ui_ValidasiGajiWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        self.pushButton_6.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.setup_table()
        
        self.pushButton_11.clicked.connect(self.approve_transfer)
        self.pushButton_10.clicked.connect(self.upload_bukti)
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
                sql = """SELECT g.id, k.nama_lengkap, g.bulan, g.tahun, g.total_gaji, g.status_transfer
                         FROM gaji g JOIN karyawan k ON g.karyawan_id = k.id
                         ORDER BY g.status_transfer ASC, g.tahun DESC, g.bulan DESC"""
                cursor.execute(sql)
                results = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for r, d in enumerate(results):
                    self.tableWidget.insertRow(r)
                    id_item = QTableWidgetItem(str(r + 1))
                    id_item.setData(Qt.UserRole, d[0])
                    self.tableWidget.setItem(r, 0, id_item)
                    self.tableWidget.setItem(r, 1, QTableWidgetItem(d[1]))
                    self.tableWidget.setItem(r, 2, QTableWidgetItem(f"{d[2]}/{d[3]}"))
                    self.tableWidget.setItem(r, 3, QTableWidgetItem(f"Rp {d[4]:,.0f}"))
                    self.tableWidget.setItem(r, 4, QTableWidgetItem(d[5]))
            finally: conn.close()

    def approve_transfer(self):
        row = self.tableWidget.currentRow()
        if row < 0: return
        gaji_id = self.tableWidget.item(row, 0).data(Qt.UserRole)
        if QMessageBox.question(self, "Konfirmasi", "Tandai SUDAH DITRANSFER?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try: 
                    cursor = conn.cursor()
                    cursor.execute("UPDATE gaji SET status_transfer='Sudah Transfer', tanggal_transfer=%s WHERE id=%s", (date.today(), gaji_id))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def upload_bukti(self):
        QMessageBox.information(self, "Info", "Fitur Upload Bukti belum diimplementasikan sepenuhnya.")

class LaporanGajiWindow(BaseWindow, Ui_LaporanGajiWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        self.populate_year_combo()
        self.setup_table()
        self.comboBox.setCurrentText(str(date.today().year))
        
        self.pushButton_5.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        
        self.pushButton_9.clicked.connect(self.load_data)
        self.pushButton_10.clicked.connect(self.export_pdf)
        QTimer.singleShot(100, self.load_data)

    def populate_year_combo(self):
        curr = date.today().year
        for y in range(curr+1, curr-5, -1):
            self.comboBox.addItem(str(y))

    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    def load_data(self):
        sel_year = self.comboBox.currentText()
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "SELECT k.nama_lengkap, k.jabatan, g.bulan, g.gaji_pokok, g.total_tunjangan, g.total_potongan, g.total_gaji, g.status_transfer FROM gaji g JOIN karyawan k ON g.karyawan_id=k.id WHERE g.tahun=%s ORDER BY g.bulan DESC"
                cursor.execute(sql, (sel_year,))
                res = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                total=0; sent=0; pending=0
                
                for r, d in enumerate(res):
                    self.tableWidget.insertRow(r)
                    self.tableWidget.setItem(r,0,QTableWidgetItem(str(r+1)))
                    self.tableWidget.setItem(r,1,QTableWidgetItem(d[0]))
                    self.tableWidget.setItem(r,2,QTableWidgetItem(d[1]))
                    self.tableWidget.setItem(r,3,QTableWidgetItem(str(d[2])))
                    self.tableWidget.setItem(r,4,QTableWidgetItem(f"{d[3]:,.0f}"))
                    self.tableWidget.setItem(r,5,QTableWidgetItem(f"{d[4]:,.0f}"))
                    self.tableWidget.setItem(r,6,QTableWidgetItem(f"{d[5]:,.0f}"))
                    self.tableWidget.setItem(r,7,QTableWidgetItem(f"{d[6]:,.0f}"))
                    self.tableWidget.setItem(r,8,QTableWidgetItem(d[7]))
                    
                    total += d[6]
                    if d[7] == 'Sudah Transfer': sent += d[6]
                    else: pending += d[6]
                    
                self.lineEdit.setText(f"Rp {total:,.0f}")
                self.lineEdit_2.setText(f"Rp {sent:,.0f}")
                self.lineEdit_3.setText(f"Rp {pending:,.0f}")
            except Exception as e: print(e)
            finally: conn.close()

    def export_pdf(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan PDF", f"Laporan_{self.comboBox.currentText()}.pdf", "PDF (*.pdf)")
        if not path: return
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT k.nama_lengkap, k.jabatan, g.bulan, g.total_gaji, g.status_transfer FROM gaji g JOIN karyawan k ON g.karyawan_id=k.id WHERE g.tahun=%s", (self.comboBox.currentText(),))
                data = cursor.fetchall()
                doc = SimpleDocTemplate(path, pagesize=landscape(letter))
                elements = []
                elements.append(Paragraph(f"<b>Laporan Gaji Tahun {self.comboBox.currentText()}</b>", getSampleStyleSheet()['Title']))
                elements.append(Spacer(1, 20))
                tbl_data = [['Nama', 'Jabatan', 'Bulan', 'Total Gaji', 'Status']]
                for row in data:
                    tbl_data.append([row[0], row[1], str(row[2]), f"Rp {row[3]:,.0f}", row[4]])
                t = Table(tbl_data)
                t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black), ('BACKGROUND',(0,0),(-1,0), colors.grey)]))
                elements.append(t)
                doc.build(elements)
                QMessageBox.information(self, "Sukses", "PDF Berhasil Disimpan")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally: conn.close()

class AbsensiAdminWindow(BaseWindow, Ui_AbsensiWindow):
    def __init__(self, previous_window=None):
        super().__init__(previous_window)
        self.setupUi(self)
        self.setup_nav()
        
        self.dateEdit.setDate(QDate.currentDate())
        self.dateEdit.setDisplayFormat("MM/yyyy")
        self.pushButton.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold; border: 1px solid #ccc;")

        self.setup_tables()
        self.pushButton_9.clicked.connect(self.load_absensi)        
        self.pushButton_10.clicked.connect(self.approve_cuti)       
        self.pushButton_11.clicked.connect(self.reject_cuti)
        QTimer.singleShot(100, self.init_data)

    def init_data(self):
        self.load_combo_karyawan()
        self.load_absensi()
        self.load_notifikasi_cuti()

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
                cursor = conn.cursor()
                cursor.execute("SELECT nama_lengkap FROM karyawan WHERE status_akun='Aktif'")
                self.comboBox.addItem("Semua Karyawan")
                for r in cursor.fetchall():
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
                cursor = conn.cursor()
                sql = "SELECT a.tanggal, k.nama_lengkap, k.jabatan, a.status FROM absensi a JOIN karyawan k ON a.karyawan_id = k.id WHERE MONTH(a.tanggal)=%s AND YEAR(a.tanggal)=%s"
                params = [bulan, tahun]
                if filter_nama != "Semua Karyawan":
                    sql += " AND k.nama_lengkap=%s"
                    params.append(filter_nama)
                sql += " ORDER BY a.tanggal DESC"
                cursor.execute(sql, tuple(params))
                results = cursor.fetchall()
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
                cursor = conn.cursor()
                sql = "SELECT c.id, k.nama_lengkap, c.tanggal_mulai, k.jabatan, c.status_validasi, c.jumlah_hari, c.alasan FROM cuti c JOIN karyawan k ON c.karyawan_id = k.id WHERE c.status_validasi='Pending'"
                cursor.execute(sql)
                results = cursor.fetchall()
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
        if row < 0: return
        cuti_id = self.tableWidget_2.item(row, 0).data(Qt.UserRole)
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE cuti SET status_validasi=%s WHERE id=%s", (status_baru, cuti_id))
                if status_baru == "Disetujui":
                    cursor.execute("SELECT karyawan_id, tanggal_mulai, jumlah_hari FROM cuti WHERE id=%s", (cuti_id,))
                    res = cursor.fetchone()
                    if res:
                        emp_id, start_date, duration = res
                        for i in range(duration):
                            curr_d = start_date + timedelta(days=i)
                            cursor.execute("SELECT id FROM absensi WHERE karyawan_id=%s AND tanggal=%s", (emp_id, curr_d))
                            if not cursor.fetchone():
                                cursor.execute("INSERT INTO absensi (karyawan_id, tanggal, status) VALUES (%s, %s, 'Cuti')", (emp_id, curr_d))
                conn.commit()
                QMessageBox.information(self, "Sukses", f"Status: {status_baru}")
                self.load_notifikasi_cuti()
                self.load_absensi()
            except Exception as e: QMessageBox.critical(self, "Error", str(e))
            finally: conn.close()

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

# --- DASHBOARD ADMIN ---
class AdminDashboard(BaseWindow, Ui_AdminWindow):
    def __init__(self):
        super().__init__(None) # Previous window = None
        self.setupUi(self)
        self.setup_nav()
        
        try: self.pushButton_2.clicked.disconnect() 
        except: pass
        self.pushButton_2.clicked.connect(self.load_dashboard_data)

        self.pushButton_2.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        QTimer.singleShot(100, self.load_dashboard_data)

    def load_dashboard_data(self):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM karyawan WHERE status_akun = 'Aktif'")
                self.label_5.setText(str(cursor.fetchone()[0]))
                cursor.execute("SELECT COUNT(*) FROM karyawan WHERE status_akun = 'Nonaktif'")
                self.label_7.setText(str(cursor.fetchone()[0]))
                cursor.execute("SELECT nama_lengkap, jabatan, status_kerja, tanggal_gabung FROM karyawan WHERE status_akun='Aktif' LIMIT 5")
                res = cursor.fetchall()
                self.tableWidget.setRowCount(0)
                for r, row in enumerate(res):
                    self.tableWidget.insertRow(r)
                    self.tableWidget.setItem(r,0,QTableWidgetItem(str(r+1)))
                    for c, d in enumerate(row):
                        self.tableWidget.setItem(r,c+1,QTableWidgetItem(str(d)))
            finally: conn.close()

# --- LOGIN & REGISTER ---
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
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM karyawan WHERE email=%s", (e,))
                if cursor.fetchone():
                    QMessageBox.warning(self, "Gagal", "Email sudah terdaftar.")
                    return
                # Default role: Baker, Kontrak
                cursor.execute("INSERT INTO karyawan (nama_lengkap, email, password, jabatan, status_kerja, status_akun, tanggal_gabung) VALUES (%s,%s,%s,'Baker','Kontrak','Aktif',%s)", (n,e,p,date.today()))
                conn.commit()
                QMessageBox.information(self, "Sukses", "Registrasi Berhasil! Silakan Login.")
                self.hide()
                self.login_window.show()
            finally: conn.close()

class EmployeeDashboard(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.setWindowTitle(f"Dashboard - {user_data['nama']}")
        self.setGeometry(100, 100, 600, 400)
        lbl = QLabel(f"Halo, {user_data['nama']}!\n(Halaman Karyawan - Sedang dikembangkan)", self)
        lbl.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(lbl)

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
                cursor = conn.cursor()
                cursor.execute("SELECT id, nama_lengkap, jabatan, status_akun FROM karyawan WHERE email=%s AND password=%s", (e,p))
                user = cursor.fetchone()
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