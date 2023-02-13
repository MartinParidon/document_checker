# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'phrase_checker.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(305, 256)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton_run = QPushButton(self.centralwidget)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(120, 200, 75, 24))
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 281, 171))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_input_folder_path = QLineEdit(self.layoutWidget)
        self.lineEdit_input_folder_path.setObjectName(u"lineEdit_input_folder_path")
        self.lineEdit_input_folder_path.setEnabled(True)
        self.lineEdit_input_folder_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_input_folder_path.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_input_folder_path, 0, 0, 1, 1)

        self.pushButton_input_folder_path = QPushButton(self.layoutWidget)
        self.pushButton_input_folder_path.setObjectName(u"pushButton_input_folder_path")

        self.gridLayout.addWidget(self.pushButton_input_folder_path, 0, 1, 1, 1)

        self.lineEdit_output_folder_path = QLineEdit(self.layoutWidget)
        self.lineEdit_output_folder_path.setObjectName(u"lineEdit_output_folder_path")
        self.lineEdit_output_folder_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_output_folder_path.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_output_folder_path, 1, 0, 1, 1)

        self.pushButton_output_folder_path = QPushButton(self.layoutWidget)
        self.pushButton_output_folder_path.setObjectName(u"pushButton_output_folder_path")

        self.gridLayout.addWidget(self.pushButton_output_folder_path, 1, 1, 1, 1)

        self.lineEdit_phrases_file_path = QLineEdit(self.layoutWidget)
        self.lineEdit_phrases_file_path.setObjectName(u"lineEdit_phrases_file_path")
        self.lineEdit_phrases_file_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_phrases_file_path.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_phrases_file_path, 2, 0, 1, 1)

        self.pushButton_phrases_file_path = QPushButton(self.layoutWidget)
        self.pushButton_phrases_file_path.setObjectName(u"pushButton_phrases_file_path")

        self.gridLayout.addWidget(self.pushButton_phrases_file_path, 2, 1, 1, 1)

        self.lineEdit_words_file_path = QLineEdit(self.layoutWidget)
        self.lineEdit_words_file_path.setObjectName(u"lineEdit_words_file_path")
        self.lineEdit_words_file_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lineEdit_words_file_path.setReadOnly(True)

        self.gridLayout.addWidget(self.lineEdit_words_file_path, 3, 0, 1, 1)

        self.pushButton_words_file_path = QPushButton(self.layoutWidget)
        self.pushButton_words_file_path.setObjectName(u"pushButton_words_file_path")

        self.gridLayout.addWidget(self.pushButton_words_file_path, 3, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 305, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Heraklit", None))
        self.pushButton_run.setText(QCoreApplication.translate("MainWindow", u"Run", None))
        self.pushButton_input_folder_path.setText(QCoreApplication.translate("MainWindow", u"Input Folder Path", None))
        self.pushButton_output_folder_path.setText(QCoreApplication.translate("MainWindow", u"Output Folder Path", None))
        self.pushButton_phrases_file_path.setText(QCoreApplication.translate("MainWindow", u"Phrases File Path", None))
        self.pushButton_words_file_path.setText(QCoreApplication.translate("MainWindow", u"Words File Path", None))
    # retranslateUi

