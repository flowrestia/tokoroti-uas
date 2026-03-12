# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ValidasiGaji.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(893, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(220, 91, 621, 51))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"font-weight: bold;\n"
"padding: 5px;\n"
"")

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalFrame = QFrame(self.centralwidget)
        self.verticalFrame.setObjectName(u"verticalFrame")
        self.verticalFrame.setGeometry(QRect(52, 82, 160, 461))
        self.verticalFrame.setStyleSheet(u"QFrame {\n"
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
        self.verticalLayout_2 = QVBoxLayout(self.verticalFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.verticalFrame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"color: #262628;\n"
"font-weight: bold;\n"
"background-color: #d6dc82;\n"
"padding: 5px;\n"
"qproperty-alignment: 'AlignCenter';")

        self.verticalLayout_2.addWidget(self.label_2)

        self.pushButton_2 = QPushButton(self.verticalFrame)
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

        self.pushButton_4 = QPushButton(self.verticalFrame)
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

        self.pushButton_3 = QPushButton(self.verticalFrame)
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

        self.pushButton = QPushButton(self.verticalFrame)
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

        self.pushButton_5 = QPushButton(self.verticalFrame)
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

        self.pushButton_6 = QPushButton(self.verticalFrame)
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

        self.pushButton_7 = QPushButton(self.verticalFrame)
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

        self.line = QFrame(self.verticalFrame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.pushButton_8 = QPushButton(self.verticalFrame)
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

        self.verticalFrame_2 = QFrame(self.centralwidget)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalFrame_2.setGeometry(QRect(52, 22, 791, 61))
        self.verticalFrame_2.setStyleSheet(u"QFrame {\n"
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
        self.verticalLayout = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.verticalFrame_2)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(220, 150, 621, 341))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableWidget = QTableWidget(self.verticalLayoutWidget_2)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
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

        self.verticalLayout_4.addWidget(self.tableWidget)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(220, 500, 621, 41))
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
        self.menubar.setGeometry(QRect(0, 0, 893, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Validasi Gaji", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Menu Admin", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Data Karyawan", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Jabatan", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Absensi", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Laporan Gaji", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Validasi Gaji", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Arsip Nonaktif", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sistem Manajemen Karyawan Toko Roti", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Nama", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Bulan", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Total", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Hapus", None))
    # retranslateUi

