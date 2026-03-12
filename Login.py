# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
#Nicolla Juan Ardhan
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(170, 80, 441, 80))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"    background-color: #d16c76;\n"
"    color: white;\n"
"    font-size: 22px;\n"
"    font-weight: bold;\n"
"    padding: 15px;\n"
"    border-radius: 4px;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"")

        self.verticalLayout.addWidget(self.label)

        self.verticalFrame_2 = QFrame(self.centralwidget)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalFrame_2.setGeometry(QRect(160, 160, 461, 141))
        self.verticalFrame_2.setStyleSheet(u"background-color: #fff6ee;\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.verticalFrame_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setStyleSheet(u"QLabel {\n"
"    color: #262628;\n"
"    font-size: 13px;\n"
"}")

        self.verticalLayout_2.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.verticalFrame_2)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(300, 27))
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"    background-color: #fff6ee;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 4px;\n"
"    padding: 6px;\n"
"    color: #262628;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #d16c76;\n"
"    background-color: #ffffff;\n"
"}")

        self.verticalLayout_2.addWidget(self.lineEdit)

        self.label_3 = QLabel(self.verticalFrame_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel {\n"
"    color: #262628;\n"
"    font-size: 13px;\n"
"}")

        self.verticalLayout_2.addWidget(self.label_3)

        self.lineEdit_2 = QLineEdit(self.verticalFrame_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setStyleSheet(u"QLineEdit {\n"
"    background-color: #fff6ee;\n"
"    border: 1px solid #ccc;\n"
"    border-radius: 4px;\n"
"    padding: 6px;\n"
"    color: #262628;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #d16c76;\n"
"    background-color: #ffffff;\n"
"}")

        self.verticalLayout_2.addWidget(self.lineEdit_2)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(170, 310, 441, 62))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.verticalLayoutWidget_3)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #fff6ee;\n"
"    border: 1px solid #d16c76;\n"
"    padding: 8px;\n"
"    border-radius: 4px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #d6dc82;\n"
"}")

        self.verticalLayout_3.addWidget(self.pushButton)

        self.label_4 = QLabel(self.verticalLayoutWidget_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel {\n"
"    color: #262628;\n"
"    font-size: 13px;\n"
"	qproperty-alignment: 'AlignCenter';\n"
"}\n"
"\n"
"QLabel:hover {\n"
"    color: #d16c76;\n"
"    font-weight: bold;\n"
"}")

        self.verticalLayout_3.addWidget(self.label_4)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(150, 60, 481, 331))
        self.widget.setStyleSheet(u"QWidget {\n"
"    background-color: #fff6ee;\n"
"    color: #262628;\n"
"    font-family: Segoe UI;\n"
"    font-size: 14px;\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.widget.raise_()
        self.verticalLayoutWidget.raise_()
        self.verticalFrame_2.raise_()
        self.verticalLayoutWidget_3.raise_()
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"LOGIN", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"LOGIN", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Belum punya akun? Daftar", None))
    # retranslateUi

