import os.path
import sqlite3
import sys
import time
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3


class InfoWindow(QMainWindow):

    def __init__(self, main):
        super().__init__()
        self.mainWindow = main
        uic.loadUi('InfoForm.ui', self)
        self.resize(main.size())
        self.setWindowTitle("Подробная информация")
        self.curentRow = None
        # self.btnCancel.clicked.connect(self.close)
        # self.btnAdd.clicked.connect(self.change)


    def close(self):
        result = QMessageBox.question(self, "Подтверждение закрытия окна",
                                      "Вы действительно хотите закрыть окно?",
                                      QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            self.mainWindow.setGeometry(self.geometry())
            self.mainWindow.show()
            self.hide()
            return True
        return False

    def closeEvent(self, e):
        self.close()
        e.ignore()
