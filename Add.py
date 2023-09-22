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


class AddWindow(QMainWindow):

    def __init__(self, main):
        super().__init__()
        self.mainWindow = main
        uic.loadUi('AddForm.ui', self)
        self.resize(main.size())
        self.setWindowTitle("Добавление элемента")
        self.btnCancel.clicked.connect(self.close)
        self.btnAdd.clicked.connect(self.add)
        self.btnAddTags.clicked.connect(self.addTags)

        self.tagsTable.setColumnCount(2)
        self.tagsTable.horizontalHeader().setStyleSheet(self.mainWindow.headerStyle)
        self.tagsTable.verticalHeader().hide()
        self.tagsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tagsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tagsTable.setColumnWidth(1, 40)
        # self.tagsTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger(0))

        self.tagsTable.setHorizontalHeaderLabels(['', ''])

    def add(self):
        if not self.price.text().isdigit():
            QMessageBox.about(self, "Ошибка", "цена продажи должна быть числом")
            return
        if not self.originalPrice.text().isdigit():
            QMessageBox.about(self, "Ошибка", "цена закупки должна быть числом")
            return
        if not self.count.text().isdigit():
            QMessageBox.about(self, "Ошибка", "Кол-во должно быть числом")
            return
        self.mainWindow.data.append(
            [self.mainWindow.freeId[0], self.itemName.text(), self.price.text(),
             self.originalPrice.text(), self.count.text(), self.type.text()])

        self.mainWindow.freeId.pop(0)

        self.mainWindow.addRow(self.mainWindow.data[-1])

        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()


        row = [int(self.mainWindow.data[-1][0]), self.mainWindow.data[-1][1].lower(), float(self.mainWindow.data[-1][2]),
               float(self.mainWindow.data[-1][3]), float(self.mainWindow.data[-1][4]), self.mainWindow.data[-1][5].lower(), self.mainWindow.currentFolder.lower()]
        print(row)
        cur.execute("INSERT INTO ItemControl VALUES(?, ?, ?, ?, ?, ?, ?);", row)
        connection.commit()

        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()
        for i in range(self.tagsTable.rowCount()):
            r = [row[0], self.tagsTable.item(i, 0).text()]
            cur.execute("INSERT INTO TagsControl VALUES(?, ?);", r)
        connection.commit()

        self.mainWindow.setGeometry(self.geometry())
        self.mainWindow.show()
        self.hide()

    def addTags(self):
        self.tagsTable.setRowCount(self.tagsTable.rowCount() + 1)
        btnClose = QPushButton()
        btnClose.setIcon(QIcon("iconClose.png"))
        btnClose.setIconSize(QSize(20, 20))
        btnClose.setStyleSheet(self.mainWindow.btnCloseStyle)
        btnClose.clicked.connect(self.Del)
        self.tagsTable.setCellWidget(self.tagsTable.rowCount() - 1, 1, btnClose)

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

    def showEvent(self, e):
        self.itemName.setText("")
        self.price.setText("")
        self.originalPrice.setText("")
        self.count.setText("")
        self.itemName.setText("")
        self.type.setText("")
        self.tagsTable.setRowCount(0)

    def closeEvent(self, e):
        self.close()
        e.ignore()

    def Del(self):
        button = QMessageBox.question(self, "Удалить тег", "Вы уверены?")
        if button == QMessageBox.StandardButton.Yes:
            row = self.tagsTable.currentRow()
            if row > -1:  # Если есть выделенная строка/элемент
                self.tagsTable.removeRow(row)
                self.tagsTable.selectionModel().clearCurrentIndex()
