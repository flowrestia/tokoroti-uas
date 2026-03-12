# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PengajuanCuti.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 580)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalFrame = QFrame(self.centralwidget)
        self.verticalFrame.setObjectName(u"verticalFrame")
        self.verticalFrame.setGeometry(QRect(0, 0, 791, 61))
        self.verticalFrame.setStyleSheet(u"QFrame {\n"
"    background-color: #d86072;\n"
"    color: #fff6ee;\n"
"    border: 1px solid #c2a600;\n"
"    font: bold 12pt \"Segoe UI\";\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QFrame:pressed {\n"
"    background-color: #ffcf33;\n"
"}\n"
"")
        self.verticalLayout = QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.verticalFrame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(170, 70, 621, 451))
        self.frame.setStyleSheet(u"background-color: rgb(255, 246, 238);")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 10, 251, 31))
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        self.label_5.setFont(font)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 50, 91, 16))
        font1 = QFont()
        font1.setBold(True)
        self.label_3.setFont(font1)
        self.horizontalLayoutWidget = QWidget(self.frame)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 70, 219, 28))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox_2 = QComboBox(self.horizontalLayoutWidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")

        self.horizontalLayout.addWidget(self.comboBox_2)

        self.comboBox = QComboBox(self.horizontalLayoutWidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")

        self.horizontalLayout.addWidget(self.comboBox)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 100, 101, 16))
        self.label_4.setFont(font1)
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(120, 100, 481, 20))
        self.lineEdit.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_7 = QLabel(self.frame)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 130, 111, 16))
        self.label_7.setFont(font1)
        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 160, 101, 16))
        self.label_9.setFont(font1)
        self.label_15 = QLabel(self.frame)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 190, 101, 16))
        self.label_15.setFont(font1)
        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setGeometry(QRect(120, 160, 481, 20))
        self.lineEdit_3.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_4 = QLineEdit(self.frame)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setGeometry(QRect(120, 190, 481, 71))
        self.lineEdit_4.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(120, 130, 481, 20))
        self.lineEdit_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.pushButton_12 = QPushButton(self.frame)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setGeometry(QRect(470, 410, 131, 31))
        self.pushButton_12.setFont(font1)
        self.pushButton_12.setStyleSheet(u"color: #ffffff;\n"
"font-weight: bold;\n"
"background-color: #d86072;\n"
"padding: 5px;\n"
"qproperty-alignment: 'AlignCenter';\n"
"")
        self.verticalFrame_2 = QFrame(self.centralwidget)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalFrame_2.setGeometry(QRect(0, 60, 160, 461))
        self.verticalFrame_2.setStyleSheet(u"QFrame {\n"
"    background-color: #d86072;\n"
"    color: #262628;\n"
"    border: 1px solid #c2a600;\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QFrame:pressed {\n"
"    background-color: #ffcf33;\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.verticalFrame_2)
        self.label_2.setObjectName(u"label_2")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(11)
        font2.setBold(True)
        font2.setItalic(False)
        self.label_2.setFont(font2)
        self.label_2.setStyleSheet(u"color: #262628;\n"
"font-weight: bold;\n"
"background-color: #d6dc82;\n"
"padding: 5px;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_2.addWidget(self.label_2)

        self.pushButton_2 = QPushButton(self.verticalFrame_2)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"	color: #262628;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.verticalFrame_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"	color: #262628;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.pushButton = QPushButton(self.verticalFrame_2)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"	color: #262628;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton)

        self.pushButton_5 = QPushButton(self.verticalFrame_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"	color: #262628;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton_5)

        self.line = QFrame(self.verticalFrame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.pushButton_8 = QPushButton(self.verticalFrame_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"	color: red;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.verticalLayout_2.addWidget(self.pushButton_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sistem Manajemen Karyawan Toko Roti", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Pengajuan Cuti", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Bulan & Tahun", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Januari", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Februari", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Maret", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"April", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Mei", None))
        self.comboBox_2.setItemText(5, QCoreApplication.translate("MainWindow", u"Juni", None))
        self.comboBox_2.setItemText(6, QCoreApplication.translate("MainWindow", u"Juli", None))
        self.comboBox_2.setItemText(7, QCoreApplication.translate("MainWindow", u"Agustus", None))
        self.comboBox_2.setItemText(8, QCoreApplication.translate("MainWindow", u"September", None))
        self.comboBox_2.setItemText(9, QCoreApplication.translate("MainWindow", u"Oktober", None))
        self.comboBox_2.setItemText(10, QCoreApplication.translate("MainWindow", u"November", None))
        self.comboBox_2.setItemText(11, QCoreApplication.translate("MainWindow", u"Desember", None))

        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"2025", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"2026", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Nama                   :", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Jabatan                :", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Jumlah Hari        :", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Alasan Cuti         :", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"Kirim", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Menu Karyawan", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Absensi", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Lihat Slip Gaji", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Riwayat Cuti ", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Pengajuan Cuti", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
    # retranslateUi

