# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ArsipNonaktif.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

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
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_2.addWidget(self.label_2)

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

        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(229, 79, 621, 401))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.gridLayoutWidget)
        if (self.tableWidget.columnCount() < 4):
            self.tableWidget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
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

        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"font-weight: bold;\n"
"padding: 5px;\n"
"")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(230, 490, 621, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_11 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setStyleSheet(u"QPushButton {\n"
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

        self.horizontalLayout.addWidget(self.pushButton_11)

        self.pushButton_10 = QPushButton(self.horizontalLayoutWidget)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setStyleSheet(u"QPushButton {\n"
"    background-color: red;\n"
"	color: white;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}\n"
"")

        self.horizontalLayout.addWidget(self.pushButton_10)

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
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Nama", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Jabatan Terakhir", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Tanggal Berhenti", None));
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Arsip Karyawan Nonaktif", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Hapus", None))
    # retranslateUi

