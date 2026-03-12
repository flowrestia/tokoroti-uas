# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DashboardAdmin.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHeaderView, QLabel,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(907, 576)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: #e8ecf1;   \n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalFrame = QFrame(self.centralwidget)
        self.verticalFrame.setObjectName(u"verticalFrame")
        self.verticalFrame.setGeometry(QRect(60, 10, 791, 61))
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

        self.verticalFrame1 = QFrame(self.centralwidget)
        self.verticalFrame1.setObjectName(u"verticalFrame1")
        self.verticalFrame1.setGeometry(QRect(60, 70, 160, 461))
        self.verticalFrame1.setStyleSheet(u"QFrame {\n"
"    background-color: #d86072;\n"
"    color: #262628;\n"
"    border: 1px solid #c2a600;\n"
"    font: bold 12pt \"Segoe UI\";\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QFrame:pressed {\n"
"    background-color: #ffcf33;\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.verticalFrame1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.verticalFrame1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: #262628;\n"
"font-weight: bold;\n"
"background-color: #d6dc82;\n"
"padding: 5px;\n"
"qproperty-alignment: 'AlignCenter';\n"
"")

        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignVCenter)

        self.pushButton_2 = QPushButton(self.verticalFrame1)
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

        self.pushButton_4 = QPushButton(self.verticalFrame1)
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

        self.pushButton_3 = QPushButton(self.verticalFrame1)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.pushButton = QPushButton(self.verticalFrame1)
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

        self.pushButton_5 = QPushButton(self.verticalFrame1)
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

        self.pushButton_6 = QPushButton(self.verticalFrame1)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.verticalFrame1)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_2.addWidget(self.pushButton_7)

        self.line = QFrame(self.verticalFrame1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.pushButton_8 = QPushButton(self.verticalFrame1)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setStyleSheet(u"color: red;\n"
"background-color: white;\n"
"border: none;\n"
"font-weight: bold;\n"
"padding: 5px;QPushButton {\n"
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

        self.verticalFrame2 = QFrame(self.centralwidget)
        self.verticalFrame2.setObjectName(u"verticalFrame2")
        self.verticalFrame2.setGeometry(QRect(230, 80, 151, 81))
        self.verticalFrame2.setStyleSheet(u"background-color: #fff6ee;\n"
"border: 1px solid #ddd;\n"
"border-radius: 10px;\n"
"padding: 3px;\n"
"")
        self.verticalLayout_3 = QVBoxLayout(self.verticalFrame2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.verticalFrame2)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"QLabel{\n"
"    font-size: 9pt;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"}\n"
"")

        self.verticalLayout_3.addWidget(self.label_4)

        self.label_5 = QLabel(self.verticalFrame2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setStyleSheet(u"padding-left: 10px;\n"
"text-align: center;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_3.addWidget(self.label_5)

        self.verticalFrame3 = QFrame(self.centralwidget)
        self.verticalFrame3.setObjectName(u"verticalFrame3")
        self.verticalFrame3.setGeometry(QRect(229, 170, 621, 16))
        font1 = QFont()
        font1.setBold(False)
        self.verticalFrame3.setFont(font1)
        self.verticalLayout_7 = QVBoxLayout(self.verticalFrame3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.line_2 = QFrame(self.verticalFrame3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFont(font1)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(229, 189, 621, 341))
        self.verticalLayout_8 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font-size: 14pt;\n"
"font-weight: bold;\n"
"padding-left: 10px;\n"
"")

        self.verticalLayout_8.addWidget(self.label_3, 0, Qt.AlignLeft|Qt.AlignVCenter)

        self.tableWidget = QTableWidget(self.verticalLayoutWidget_2)
        if (self.tableWidget.columnCount() < 6):
            self.tableWidget.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setStyleSheet(u"QHeaderView::section {\n"
"    background-color: #d6dc82;\n"
"    color: black;\n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    background-color: #fff6ee;\n"
"    gridline-color: #ccc;\n"
"    border: 1px solid #ddd;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #ffe5b4;\n"
"    color: black;\n"
"}\n"
"")

        self.verticalLayout_8.addWidget(self.tableWidget)

        self.verticalFrame_2 = QFrame(self.centralwidget)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalFrame_2.setGeometry(QRect(390, 80, 151, 81))
        self.verticalFrame_2.setStyleSheet(u"background-color: #fff6ee;\n"
"border: 1px solid #ddd;\n"
"border-radius: 10px;\n"
"padding: 3px;\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_6 = QLabel(self.verticalFrame_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(u"QLabel{\n"
"    font-size: 9pt;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"}\n"
"")

        self.verticalLayout_4.addWidget(self.label_6)

        self.label_7 = QLabel(self.verticalFrame_2)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"padding-left: 10px;\n"
"text-align: center;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_4.addWidget(self.label_7)

        self.verticalFrame_3 = QFrame(self.centralwidget)
        self.verticalFrame_3.setObjectName(u"verticalFrame_3")
        self.verticalFrame_3.setGeometry(QRect(550, 80, 151, 81))
        self.verticalFrame_3.setStyleSheet(u"background-color: #fff6ee;\n"
"border: 1px solid #ddd;\n"
"border-radius: 10px;\n"
"padding: 3px;\n"
"")
        self.verticalLayout_5 = QVBoxLayout(self.verticalFrame_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_8 = QLabel(self.verticalFrame_3)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(u"QLabel{\n"
"    font-size: 9pt;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"}\n"
"")

        self.verticalLayout_5.addWidget(self.label_8)

        self.label_9 = QLabel(self.verticalFrame_3)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"padding-left: 10px;\n"
"text-align: center;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_5.addWidget(self.label_9)

        self.verticalFrame_4 = QFrame(self.centralwidget)
        self.verticalFrame_4.setObjectName(u"verticalFrame_4")
        self.verticalFrame_4.setGeometry(QRect(710, 80, 141, 81))
        self.verticalFrame_4.setStyleSheet(u"background-color: #fff6ee;\n"
"border: 1px solid #ddd;\n"
"border-radius: 10px;\n"
"padding: 3px;\n"
"")
        self.verticalLayout_6 = QVBoxLayout(self.verticalFrame_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_10 = QLabel(self.verticalFrame_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"QLabel{\n"
"    font-size: 9pt;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"}\n"
"")

        self.verticalLayout_6.addWidget(self.label_10)

        self.label_11 = QLabel(self.verticalFrame_4)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setStyleSheet(u"padding-left: 10px;\n"
"text-align: center;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_6.addWidget(self.label_11)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 907, 22))
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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Menu Admin", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Data Karyawan", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Jabatan", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Absensi", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Laporan Gaji", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Validasi Gaji", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Arsip Nonaktif", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Karyawan Aktif", None))
        self.label_5.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Dashboard Admin", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Nama", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Jabatan", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Tanggal Mulai", None));
        ___qtablewidgetitem5 = self.tableWidget.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Aksi", None));
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Karyawan Nonaktif", None))
        self.label_7.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Total Gaji Bulan Ini", None))
        self.label_9.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Validasi Gaji", None))
        self.label_11.setText("")
    # retranslateUi

