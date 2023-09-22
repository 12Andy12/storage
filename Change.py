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


class ChangeWindow(QMainWindow):

    def __init__(self, main):
        super().__init__()
        self.mainWindow = main
        uic.loadUi('ChangeForm.ui', self)
        self.resize(main.size())
        self.setWindowTitle("Изменение элемента")
        self.curentRow = None
        self.btnCancel.clicked.connect(self.close)
        self.btnAdd.clicked.connect(self.change)
        self.btnAddTags.clicked.connect(self.addTags)

        self.tagsTable.setColumnCount(2)
        self.tagsTable.horizontalHeader().setStyleSheet(self.mainWindow.headerStyle)
        self.tagsTable.verticalHeader().hide()
        self.tagsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tagsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tagsTable.setColumnWidth(1, 40)
        self.tagsTable.setHorizontalHeaderLabels(['', ''])




    def change(self):
        if not self.price.text().isdigit():
            QMessageBox.about(self, "Ошибка", "цена продажи должна быть числом")
            return
        if not self.originalPrice.text().isdigit():
            QMessageBox.about(self, "Ошибка", "цена закупки должна быть числом")
            return
        if not self.count.text().isdigit():
            QMessageBox.about(self, "Ошибка", "Кол-во должно быть числом")
            return
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()
        cur.execute(
            "UPDATE ItemControl SET name = ?, price = ?, originalPrice = ?, count = ?, type = ? WHERE id = ?",
            (self.itemName.text(), self.price.text(), self.originalPrice.text(), self.count.text(),
             self.type.text(),
             int(self.mainWindow.tableWidget.item(self.curentRow, 0).text())))
        connection.commit()
        curentData = [self.mainWindow.tableWidget.item(self.curentRow, 0).text(), self.itemName.text(),
                      self.price.text(), self.originalPrice.text(), self.count.text(), self.type.text()]
        self.mainWindow.updateRow(curentData, self.curentRow)

        curentId = int(self.mainWindow.tableWidget.item(self.curentRow, 0).text())
        # connection = sqlite3.connect("ItemDataBase.db")
        # cur = connection.cursor()

        cur.execute("DELETE FROM TagsControl WHERE id = ?", (curentId, ))
        connection.commit()

        # connection = sqlite3.connect("ItemDataBase.db")
        # cur = connection.cursor()
        for i in range(self.tagsTable.rowCount()):
            if self.tagsTable.item(i, 0) is None:
                continue
            r = [curentId, self.tagsTable.item(i, 0).text()]
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
