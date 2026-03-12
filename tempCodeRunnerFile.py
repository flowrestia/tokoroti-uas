import sys
import mysql.connector
from datetime import date, datetime, timedelta

# --- IMPORT LIBRARY UI ---
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel,
                               QDialog, QFormLayout, QComboBox, QLineEdit, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QFileDialog, QSizePolicy)
from PySide6.QtCore import Qt, QDate

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
                    tanggal_transfer DATE,
                    bukti_transfer VARCHAR(255),
                    FOREIGN KEY (karyawan_id) REFERENCES karyawan(id) ON DELETE CASCADE
                )
            """)
            
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
        self.pushButton_6.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;") 
        
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_7.clicked.connect(self.open_arsip) 
        self.pushButton_8.clicked.connect(self.handle_logout)
        
        self.pushButton_11.clicked.connect(self.approve_transfer)
        self.pushButton_10.clicked.connect(self.upload_bukti)

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
                    cur=conn.cursor()
                    cur.execute("UPDATE gaji SET status_transfer='Sudah Transfer', tanggal_transfer=%s WHERE id=%s", (date.today(), gaji_id))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def upload_bukti(self):
        QMessageBox.information(self, "Info", "Fitur Upload Bukti belum diimplementasikan sepenuhnya.")

    def open_data_karyawan(self): self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_jabatan(self): self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_absensi(self): self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_laporan(self): self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()

# --- WINDOW: LAPORAN GAJI ---
class LaporanGajiWindow(QMainWindow, Ui_LaporanGajiWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window
        self.populate_year_combo()
        self.setup_table()
        self.comboBox.setCurrentText(str(date.today().year))
        
        self.pushButton_5.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_7.clicked.connect(self.open_arsip)
        self.pushButton_8.clicked.connect(self.handle_logout)
        self.pushButton_9.clicked.connect(self.load_data)
        self.pushButton_10.clicked.connect(self.export_pdf)
        
        self.load_data()

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
                cur = conn.cursor()
                sql = "SELECT k.nama_lengkap, k.jabatan, g.bulan, g.gaji_pokok, g.total_tunjangan, g.total_potongan, g.total_gaji, g.status_transfer FROM gaji g JOIN karyawan k ON g.karyawan_id=k.id WHERE g.tahun=%s ORDER BY g.bulan DESC"
                cur.execute(sql, (sel_year,))
                res = cur.fetchall()
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
                cur = conn.cursor()
                cur.execute("SELECT k.nama_lengkap, k.jabatan, g.bulan, g.total_gaji, g.status_transfer FROM gaji g JOIN karyawan k ON g.karyawan_id=k.id WHERE g.tahun=%s", (self.comboBox.currentText(),))
                data = cur.fetchall()
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

# --- WINDOW: JABATAN ---
class JabatanWindow(QMainWindow, Ui_JabatanWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window
        self.setup_table()
        self.load_data()
        self.pushButton_3.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_4.clicked.connect(self.open_data_karyawan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_7.clicked.connect(self.open_arsip)
        self.pushButton_8.clicked.connect(self.handle_logout)
        
        self.pushButton_9.clicked.connect(self.handle_add)
        self.pushButton_11.clicked.connect(self.handle_edit)
        self.pushButton_10.clicked.connect(self.handle_delete)

    def setup_table(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran FROM jabatan")
                res = cur.fetchall()
                self.tableWidget.setRowCount(0)
                for r, d in enumerate(res):
                    self.tableWidget.insertRow(r)
                    it = QTableWidgetItem(str(r+1))
                    it.setData(Qt.UserRole, d[0])
                    self.tableWidget.setItem(r,0,it)
                    self.tableWidget.setItem(r,1,QTableWidgetItem(d[1]))
                    self.tableWidget.setItem(r,2,QTableWidgetItem(f"{d[2]:,.0f}"))
                    self.tableWidget.setItem(r,3,QTableWidgetItem(f"{d[3]:,.0f}"))
                    self.tableWidget.setItem(r,4,QTableWidgetItem(f"{d[4]:,.0f}"))
            finally: conn.close()

    def handle_add(self):
        d = JabatanDialog(self)
        if d.exec() == QDialog.Accepted:
            dat = d.get_data()
            conn = create_connection()
            if conn:
                try: 
                    cur=conn.cursor()
                    cur.execute("INSERT INTO jabatan (nama_jabatan, gaji_pokok, tunjangan_jabatan, tunjangan_kehadiran) VALUES (%s,%s,%s,%s)", (dat['nama'], dat['gaji'], dat['tunj_jab'], dat['tunj_hadir']))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def handle_edit(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        idj = self.tableWidget.item(r,0).data(Qt.UserRole)
        # Hapus koma agar bisa diconvert float
        old = {
            'nama': self.tableWidget.item(r,1).text(), 
            'gaji': self.tableWidget.item(r,2).text().replace(",",""), 
            'tunj_jab': self.tableWidget.item(r,3).text().replace(",",""), 
            'tunj_hadir': self.tableWidget.item(r,4).text().replace(",","")
        }
        d = JabatanDialog(self, old)
        if d.exec() == QDialog.Accepted:
            dat = d.get_data()
            conn = create_connection()
            if conn:
                try: 
                    cur=conn.cursor()
                    cur.execute("UPDATE jabatan SET nama_jabatan=%s, gaji_pokok=%s, tunjangan_jabatan=%s, tunjangan_kehadiran=%s WHERE id=%s", (dat['nama'], dat['gaji'], dat['tunj_jab'], dat['tunj_hadir'], idj))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def handle_delete(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        if QMessageBox.question(self, "Hapus", "Yakin?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try: 
                    cur=conn.cursor()
                    cur.execute("DELETE FROM jabatan WHERE id=%s", (self.tableWidget.item(r,0).data(Qt.UserRole),))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def open_data_karyawan(self): self.hide(); self.win = DataKaryawanWindow(self.previous_window); self.win.show()
    def open_absensi(self): self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_laporan(self): self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_validasi(self): self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()

# --- WINDOW: DATA KARYAWAN ---
class DataKaryawanWindow(QMainWindow, Ui_DataKaryawanWindow):
    def __init__(self, previous_window=None):
        super().__init__()
        self.setupUi(self)
        self.previous_window = previous_window
        self.setup_table_behavior()
        self.load_data()
        self.pushButton_4.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")
        
        self.pushButton_2.clicked.connect(self.back_to_dashboard)
        self.pushButton_3.clicked.connect(self.open_jabatan)
        self.pushButton.clicked.connect(self.open_absensi)
        self.pushButton_5.clicked.connect(self.open_laporan)
        self.pushButton_6.clicked.connect(self.open_validasi)
        self.pushButton_7.clicked.connect(self.open_arsip)
        self.pushButton_8.clicked.connect(self.handle_logout)
        
        self.pushButton_9.clicked.connect(self.open_add_employee)
        self.pushButton_11.clicked.connect(self.handle_edit)
        self.pushButton_10.clicked.connect(self.handle_delete)

    def setup_table_behavior(self):
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)

    def load_data(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, nama_lengkap, jabatan, status_kerja, tanggal_gabung, status_akun FROM karyawan WHERE status_akun='Aktif'")
                res = cur.fetchall()
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

    def handle_edit(self):
        r = self.tableWidget.currentRow()
        if r < 0:
            QMessageBox.warning(self, "Info", "Pilih Baris")
            return
        idk = self.tableWidget.item(r,0).data(Qt.UserRole)
        curr = {'nama': self.tableWidget.item(r,1).text(), 'jabatan': self.tableWidget.item(r,2).text(), 'status_kerja': self.tableWidget.item(r,3).text(), 'status_akun': self.tableWidget.item(r,5).text()}
        d = EditEmployeeDialog(self, curr)
        if d.exec() == QDialog.Accepted:
            new = d.get_updated_data()
            conn = create_connection()
            if conn:
                try: 
                    cur=conn.cursor()
                    cur.execute("UPDATE karyawan SET nama_lengkap=%s, jabatan=%s, status_kerja=%s, status_akun=%s WHERE id=%s", (new['nama'], new['jabatan'], new['status_kerja'], new['status_akun'], idk))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def handle_delete(self):
        r = self.tableWidget.currentRow()
        if r < 0: return
        idk = self.tableWidget.item(r,0).data(Qt.UserRole)
        if QMessageBox.question(self, "Hapus", "Pindahkan ke Arsip (Nonaktif)?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            conn = create_connection()
            if conn:
                try: 
                    cur=conn.cursor()
                    cur.execute("UPDATE karyawan SET status_akun='Nonaktif' WHERE id=%s", (idk,))
                    conn.commit()
                    self.load_data()
                except: pass
                finally: conn.close()

    def open_add_employee(self): QMessageBox.information(self, "Info", "Gunakan Register di Login")
    def open_jabatan(self): self.hide(); self.win = JabatanWindow(self.previous_window); self.win.show()
    def open_absensi(self): self.hide(); self.win = AbsensiAdminWindow(self.previous_window); self.win.show()
    def open_laporan(self): self.hide(); self.win = LaporanGajiWindow(self.previous_window); self.win.show()
    def open_validasi(self): self.hide(); self.win = ValidasiGajiWindow(self.previous_window); self.win.show()
    def open_arsip(self): self.hide(); self.win = ArsipNonaktifWindow(self.previous_window); self.win.show()
    def back_to_dashboard(self): self.hide(); self.previous_window.load_dashboard_data(); self.previous_window.show()
    def handle_logout(self): self.close(); global window; window.show()

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

# --- EMPLOYEE DASHBOARD (Placeholder) ---
class EmployeeDashboard(QMainWindow, Ui_AbsensiKaryawanWindow):
    def __init__(self, user_data):
        super().__init__()
        self.setupUi(self)
        self.user = user_data

        # UI tweaks
        self.label_15.setText(f"Sistem Manajemen Karyawan Toko Roti - {self.user['nama']}")
        self.pushButton_2.setStyleSheet("background-color: #d6dc82; color: #262628; font-weight: bold;")

        # Table setup
        self.tableWidget_3.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_3.setSelectionMode(QAbstractItemView.SingleSelection)

        # Load data
        self.load_absensi_history()

        # Connect buttons
        self.pushButton_14.clicked.connect(self.absen_datang)
        self.pushButton_6.clicked.connect(self.absen_pulang)
        self.pushButton_4.clicked.connect(self.open_slip_gaji)
        self.pushButton.clicked.connect(self.open_riwayat_cuti)
        self.pushButton_5.clicked.connect(self.open_pengajuan_cuti)
        self.pushButton_8.clicked.connect(self.handle_logout)

    def load_absensi_history(self):
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                sql = "SELECT tanggal, waktu_masuk, waktu_pulang, status FROM absensi WHERE karyawan_id=%s ORDER BY tanggal DESC LIMIT 200"
                cur.execute(sql, (self.user['id'],))
                res = cur.fetchall()
                self.tableWidget_3.setRowCount(0)
                for r, row in enumerate(res):
                    self.tableWidget_3.insertRow(r)
                    self.tableWidget_3.setItem(r, 0, QTableWidgetItem(str(r+1)))
                    tgl = row[0].strftime("%d-%m-%Y") if row[0] else "-"
                    self.tableWidget_3.setItem(r, 1, QTableWidgetItem(tgl))
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
                cur.execute("SELECT id, waktu_masuk FROM absensi WHERE karyawan_id=%s AND tanggal=%s", (self.user['id'], today))
                row = cur.fetchone()
                if row:
                    if row[1]:
                        QMessageBox.information(self, "Info", "Anda sudah absen datang hari ini.")
                    else:
                        cur.execute("UPDATE absensi SET waktu_masuk=%s, status=%s WHERE id=%s", (now, 'Hadir', row[0]))
                        conn.commit()
                        QMessageBox.information(self, "Sukses", "Absen datang tercatat.")
                else:
                    cur.execute("INSERT INTO absensi (karyawan_id, tanggal, waktu_masuk, status) VALUES (%s,%s,%s,%s)", (self.user['id'], today, now, 'Hadir'))
                    conn.commit()
                    QMessageBox.information(self, "Sukses", "Absen datang tercatat.")
                self.load_absensi_history()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    def absen_pulang(self):
        today = date.today()
        now = datetime.now().strftime("%H:%M:%S")
        conn = create_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("SELECT id, waktu_pulang FROM absensi WHERE karyawan_id=%s AND tanggal=%s", (self.user['id'], today))
                row = cur.fetchone()
                if row:
                    if row[1]:
                        QMessageBox.information(self, "Info", "Anda sudah absen pulang hari ini.")
                    else:
                        cur.execute("UPDATE absensi SET waktu_pulang=%s WHERE id=%s", (now, row[0]))
                        conn.commit()
                        QMessageBox.information(self, "Sukses", "Absen pulang tercatat.")
                else:
                    QMessageBox.warning(self, "Warning", "Belum melakukan absen datang. Silakan absen datang terlebih dahulu.")
                self.load_absensi_history()
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            finally:
                conn.close()

    def open_slip_gaji(self):
        if not hasattr(self, 'slip_window') or self.slip_window is None:
            self.slip_window = SlipGajiWindow(self.user)
        self.slip_window.load_slip()
        self.slip_window.show()
    def open_riwayat_cuti(self):
        if not hasattr(self, 'riwayat_window') or self.riwayat_window is None:
            self.riwayat_window = RiwayatCutiWindow(self.user)
        self.riwayat_window.load_data()
        self.riwayat_window.show()

    def open_pengajuan_cuti(self):
        if not hasattr(self, 'pengajuan_window') or self.pengajuan_window is None:
            self.pengajuan_window = PengajuanCutiWindow(self.user)
        self.pengajuan_window.show()

    def handle_logout(self):
        self.close()
        global window
        window.show()

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


    class PengajuanCutiWindow(QMainWindow, Ui_PengajuanCutiWindow):
        def __init__(self, user):
            super().__init__()
            self.setupUi(self)
            self.user = user
            # Fill basic info
            try:
                self.lineEdit.setText(self.user['nama'])
                self.lineEdit_2.setText(self.user['jabatan'])
            except: pass
            # connect send
            self.pushButton_12.clicked.connect(self.send_pengajuan)
            self.pushButton_8.clicked.connect(self.close)

        def send_pengajuan(self):
            bulan_idx = self.comboBox_2.currentIndex() + 1
            tahun = int(self.comboBox.currentText())
            jumlah = self.lineEdit_3.text()
            alasan = self.lineEdit_4.text()
            if not jumlah or not alasan:
                QMessageBox.warning(self, 'Info', 'Isi semua field.')
                return
            try:
                jumlah_int = int(jumlah)
            except:
                QMessageBox.warning(self, 'Info', 'Jumlah hari harus angka.')
                return
            tanggal_mulai = date(tahun, bulan_idx, 1)
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("INSERT INTO cuti (karyawan_id, tanggal_mulai, jumlah_hari, alasan, status_validasi) VALUES (%s,%s,%s,%s,'Pending')",
                                (self.user['id'], tanggal_mulai, jumlah_int, alasan))
                    conn.commit()
                    QMessageBox.information(self, 'Sukses', 'Pengajuan cuti dikirim.')
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, 'Error', str(e))
                finally:
                    conn.close()


    class RiwayatCutiWindow(QMainWindow, Ui_RiwayatCutiWindow):
        def __init__(self, user):
            super().__init__()
            self.setupUi(self)
            self.user = user
            self.pushButton_8.clicked.connect(self.close)

        def load_data(self):
            self.tableWidget_3.setRowCount(0)
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT tanggal_mulai, jumlah_hari, alasan, status_validasi FROM cuti WHERE karyawan_id=%s ORDER BY tanggal_mulai DESC", (self.user['id'],))
                    res = cur.fetchall()
                    for r, row in enumerate(res):
                        self.tableWidget_3.insertRow(r)
                        self.tableWidget_3.setItem(r, 0, QTableWidgetItem(str(r+1)))
                        tgl = row[0].strftime('%d-%m-%Y') if row[0] else '-'
                        self.tableWidget_3.setItem(r, 1, QTableWidgetItem(tgl))
                        self.tableWidget_3.setItem(r, 2, QTableWidgetItem(self.user.get('nama', '')))
                        self.tableWidget_3.setItem(r, 3, QTableWidgetItem(str(row[1])))
                        self.tableWidget_3.setItem(r, 4, QTableWidgetItem(str(row[2])))
                        self.tableWidget_3.setItem(r, 5, QTableWidgetItem(str(row[3])))
                finally:
                    conn.close()


    class SlipGajiWindow(QMainWindow, Ui_SlipGajiWindow):
        def __init__(self, user):
            super().__init__()
            self.setupUi(self)
            self.user = user
            # basic fills
            try:
                self.lineEdit.setText(self.user['nama'])
                self.lineEdit_2.setText(self.user['jabatan'])
            except: pass
            self.dateEdit.setDate(QDate.currentDate())
            self.pushButton_10.clicked.connect(self.print_slip)
            self.pushButton_11.clicked.connect(self.close)

        def load_slip(self):
            month = self.comboBox_2.currentIndex() + 1
            year = int(self.comboBox.currentText())
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT gaji_pokok, total_tunjangan, total_potongan, total_gaji FROM gaji WHERE karyawan_id=%s AND bulan=%s AND tahun=%s",
                                (self.user['id'], month, year))
                    res = cur.fetchone()
                    if res:
                        self.lineEdit_3.setText(f"{res[0]:,.0f}")
                        self.lineEdit_4.setText(f"{res[1]:,.0f}")
                        self.lineEdit_5.setText(f"{res[2]:,.0f}")
                        self.lineEdit_6.setText("")
                        self.lineEdit_7.setText("")
                        self.lineEdit_8.setText(f"{res[3]:,.0f}")
                        self.label_5.setText(f"Slip Gaji Karyawan - {month}/{year}")
                    else:
                        self.lineEdit_3.setText("")
                        self.lineEdit_4.setText("")
                        self.lineEdit_5.setText("")
                        self.lineEdit_6.setText("")
                        self.lineEdit_7.setText("")
                        self.lineEdit_8.setText("")
                        self.label_5.setText(f"Slip Gaji Karyawan - {month}/{year} (Tidak Ada Data)")
                finally:
                    conn.close()

        def print_slip(self):
            month = self.comboBox_2.currentIndex() + 1
            year = int(self.comboBox.currentText())
            conn = create_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT total_gaji FROM gaji WHERE karyawan_id=%s AND bulan=%s AND tahun=%s", (self.user['id'], month, year))
                    res = cur.fetchone()
                    if not res:
                        QMessageBox.warning(self, 'Info', 'Tidak ada data gaji untuk periode ini.')
                        return
                    # Simple PDF export
                    filename, _ = QFileDialog.getSaveFileName(self, 'Simpan PDF', f"slip_{self.user['id']}_{month}_{year}.pdf", 'PDF Files (*.pdf)')
                    if not filename: return
                    doc = SimpleDocTemplate(filename, pagesize=letter)
                    styles = getSampleStyleSheet()
                    elems = [Paragraph(f"Slip Gaji - {self.user['nama']} ({month}/{year})", styles['Title']), Spacer(1,12),
                             Paragraph(f"Total Gaji: Rp {res[0]:,.0f}", styles['Normal'])]
                    doc.build(elems)
                    QMessageBox.information(self, 'Sukses', 'PDF disimpan.')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', str(e))
                finally:
                    conn.close()

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


class PengajuanCutiWindow(QMainWindow, Ui_PengajuanCutiWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user

        self.lineEdit.setText(self.user['nama'])
        self.lineEdit_2.setText(self.user['jabatan'])

        self.pushButton_12.clicked.connect(self.send_pengajuan)
        self.pushButton_8.clicked.connect(self.close)

    def send_pengajuan(self):
        bulan = self.comboBox_2.currentIndex() + 1
        tahun = int(self.comboBox.currentText())
        jumlah = self.lineEdit_3.text()
        alasan = self.lineEdit_4.text()

        if not jumlah or not alasan:
            QMessageBox.warning(self, "Info", "Lengkapi data.")
            return

        tanggal_mulai = date(tahun, bulan, 1)

        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO cuti (karyawan_id, tanggal_mulai, jumlah_hari, alasan)
                VALUES (%s,%s,%s,%s)
            """, (self.user['id'], tanggal_mulai, int(jumlah), alasan))
            conn.commit()
            conn.close()

        QMessageBox.information(self, "Sukses", "Pengajuan cuti dikirim.")
        self.close()

class RiwayatCutiWindow(QMainWindow, Ui_RiwayatCutiWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.pushButton_8.clicked.connect(self.close)

    def load_data(self):
        self.tableWidget_3.setRowCount(0)
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT tanggal_mulai, jumlah_hari, alasan, status_validasi
                FROM cuti
                WHERE karyawan_id=%s
                ORDER BY tanggal_mulai DESC
            """, (self.user['id'],))
            for r, d in enumerate(cur.fetchall()):
                self.tableWidget_3.insertRow(r)
                self.tableWidget_3.setItem(r,0,QTableWidgetItem(str(r+1)))
                # Tanggal
                self.tableWidget_3.setItem(r,1,QTableWidgetItem(d[0].strftime("%d-%m-%Y")))
                # Nama (dari user yang sedang login)
                self.tableWidget_3.setItem(r,2,QTableWidgetItem(self.user.get('nama', '')))
                # Jumlah Hari, Alasan, Status
                self.tableWidget_3.setItem(r,3,QTableWidgetItem(str(d[1])))
                self.tableWidget_3.setItem(r,4,QTableWidgetItem(d[2]))
                self.tableWidget_3.setItem(r,5,QTableWidgetItem(d[3]))
            conn.close()

class SlipGajiWindow(QMainWindow, Ui_SlipGajiWindow):
    def __init__(self, user):
        super().__init__()
        self.setupUi(self)
        self.user = user
        self.pushButton_8.clicked.connect(self.close)

    def load_slip(self):
        conn = create_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT bulan, tahun, total_gaji, status_transfer
                FROM gaji
                WHERE karyawan_id=%s
                ORDER BY tahun DESC, bulan DESC
                LIMIT 1
            """, (self.user['id'],))
            row = cur.fetchone()
            conn.close()

            if row:
                self.label_5.setText(f"{row[0]}/{row[1]}")
                self.label_6.setText(f"Rp {row[2]:,.0f}")
                self.label_7.setText(row[3])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    init_all_tables() 
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())