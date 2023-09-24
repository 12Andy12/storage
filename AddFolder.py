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


class AddFolderWindow(QMainWindow):

    def __init__(self, main):
        super().__init__()
        self.mainWindow = main
        uic.loadUi('AddFolderForm.ui', self)
        self.resize(main.size())
        self.setWindowTitle("Добавление папки")
        self.currentRow = None
        self.btnCancel.clicked.connect(self.close)
        self.btnAdd.clicked.connect(self.add)

    def add(self):
        # self.newFolderName.text()
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()
        cur.execute("INSERT INTO FolderControl VALUES(?, ?);",
                    (self.newFolderName.text(), self.mainWindow.currentFolder, ))
        connection.commit()
        self.mainWindow.path.pop()
        self.mainWindow.openFolder(self.mainWindow.currentFolder)
        self.mainWindow.setGeometry(self.geometry())
        self.mainWindow.show()
        self.hide()

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
