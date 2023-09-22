import os.path
import sqlite3
import sys
import time
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3
import Add
import Change
import Info
import AddFolder
import ChangeFolder
import queue

class PushButton(QtWidgets.QPushButton):
    doubleClick = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClick.emit()
            print('doubleClick')

        QtWidgets.QPushButton.mousePressEvent(self, event)


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.lastRow = None
        self.tableStyle = "QTableWidget{\ngridline-color: #666666}"
        self.headerStyle = "::section:pressed {background-color: #323232;\nborder: none;}\n::section {background-color: #323232;\nborder: none;}"
        self.btnCloseStyle = ":hover{\nbackground-color: darkred;\n}\n:pressed{\nbackground-color: red;\n}\nQPushButton{border:none}"
        self.btnChangeStyle = ":hover{\nbackground-color: darkorange;\n}\n:pressed{\nbackground-color: orange;\n}\nQPushButton{border:none}"
        self.btnOpenStyle = ':hover{\nbackground-color: darkgreen;\n}\n:pressed{\nbackground-color: green;\n}\nQPushButton{border:none} '
        self.btnFolderStyle = ':hover{\nbackground-color: darkgreen;\n}\n:pressed{\nbackground-color: green;\n}\nQPushButton{border:none;\ntext-align: left;\nfont: 20px;} '

        uic.loadUi('main.ui', self)

        self.currentFolder = "root"
        self.path = []
        self.path.append(self.currentFolder)
        self.folderLabel.setText("Текущая категория: " + self.currentFolder)

        self.setWindowTitle("Сюда вставить название")
        self.addWindow = Add.AddWindow(self)
        self.changeWindow = Change.ChangeWindow(self)
        self.infoWindow = Info.InfoWindow(self)
        self.addFolderWindow = AddFolder.AddFolderWindow(self)
        self.changeFolderWindow = ChangeFolder.ChangeFolderWindow(self)
        self.btnBack.setEnabled(False)
        self.freeId = list(range(0, 10000))
        self.fillUsedId()
        self.openFolder("root")
        self.btnBack.clicked.connect(self.fackGoBack)
        self.btnAdd.clicked.connect(self.openAddForm)
        self.btnSearch.clicked.connect(self.search)
        self.btnAddFolder.clicked.connect(self.openAddFolderForm)

    def openInfoForm(self):
        self.infoWindow.setGeometry(self.geometry())
        self.infoWindow.show()
        self.hide()

    def openAddFolderForm(self):
        self.addFolderWindow.setGeometry(self.geometry())
        self.addFolderWindow.show()
        self.hide()

    def openAddForm(self):
        self.addWindow.setGeometry(self.geometry())
        self.addWindow.show()
        self.hide()

    def openChangeForm(self):
        curentRow = self.tableWidget.currentRow()
        self.changeWindow.curentRow = curentRow
        self.changeWindow.itemName.setText(self.tableWidget.item(curentRow, 1).text())
        self.changeWindow.price.setText(self.tableWidget.item(curentRow, 2).text())
        self.changeWindow.originalPrice.setText(self.tableWidget.item(curentRow, 3).text())
        self.changeWindow.count.setText(self.tableWidget.item(curentRow, 4).text())
        self.changeWindow.type.setText(self.tableWidget.item(curentRow, 5).text())

        self.changeWindow.tagsTable.setRowCount(0)
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()

        for row in cur.execute("SELECT * FROM TagsControl WHERE id = ?", (self.tableWidget.item(curentRow, 0).text(),)):
            self.changeWindow.tagsTable.setRowCount(self.changeWindow.tagsTable.rowCount() + 1)
            self.changeWindow.tagsTable.setItem(self.changeWindow.tagsTable.rowCount() - 1, 0,
                                                QtWidgets.QTableWidgetItem(row[1]))
            btnClose = QPushButton()
            btnClose.setIcon(QIcon("iconClose.png"))
            btnClose.setIconSize(QSize(20, 20))
            btnClose.setStyleSheet(self.btnCloseStyle)
            btnClose.clicked.connect(self.changeWindow.Del)
            self.changeWindow.tagsTable.setCellWidget(self.changeWindow.tagsTable.rowCount() - 1, 1, btnClose)

        self.changeWindow.setGeometry(self.geometry())
        self.changeWindow.show()
        self.hide()

    def search(self):
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()
        request = self.searchLine.text()
        if request == "":
            ex = cur.execute("SELECT id FROM ItemControl")
        else:
            ex = cur.execute("SELECT id FROM ItemControl WHERE name = ?", (request,))

        searchId = set()
        for id in ex:
            searchId.add(id)

        if request == "":
            ex = cur.execute("SELECT id FROM ItemControl")
        else:
            ex = cur.execute("SELECT id FROM TagsControl WHERE tags = ?", (request,))

        for id in ex:
            searchId.add(id)

        self.tableWidget.setRowCount(0)

        for id in sorted(searchId):
            print(f"id = {id}\n")
            curentRow = []
            for row in cur.execute("SELECT * FROM ItemControl WHERE id = ?", id):
                for i in range(6):
                    curentRow.append(row[i])
                print(curentRow)
                self.addRow(curentRow)

    def loadTable(self):
        self.tableWidget.horizontalHeader().setStyleSheet(self.headerStyle)
        self.tableWidget.setStyleSheet(self.tableStyle)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setColumnCount(9)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(2, 80)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 80)
        self.tableWidget.setColumnWidth(5, 80)
        self.tableWidget.setColumnWidth(6, 40)
        self.tableWidget.setColumnWidth(7, 40)
        self.tableWidget.setColumnWidth(8, 40)

        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger(0))

        self.tableWidget.setHorizontalHeaderLabels(
            ['', '', '', '', '', '', '', '', ''])
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.tableWidget.horizontalHeaderItem(1).setAligment(Qt.AlignmentFlag.AlignCenter)
        self.tableWidget.horizontalHeaderItem(1).setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.tableWidget.setRowCount(0)

        headers = ['Категории', '', '', '', '', '', '', '', '']
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(str(headers[0])))
        self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 9)
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setTextAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        for currentFolder in self.folders:
            self.addFolder(currentFolder)

        headers = ['ID', 'Наименование товара', 'Цена', 'Зк. цена', 'Кол-во', '', '', '', '']
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 9)
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 9)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0, QtWidgets.QTableWidgetItem("Товары"))
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setTextAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        for i in range(6):
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, QtWidgets.QTableWidgetItem(str(headers[i])))
        self.tableWidget.item(self.tableWidget.rowCount() - 1, 1).setTextAlignment(
            QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        for currentData in self.data:
            self.addRow(currentData)

    def addFolder(self, currentFolder):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setSpan(self.tableWidget.rowCount() - 1, 0, 1, 7)

        btnFolder = PushButton()
        btnFolder.setIcon(QIcon("iconFolder.png"))
        btnFolder.setIconSize(QSize(40, 40))
        btnFolder.setStyleSheet(self.btnFolderStyle)
        btnFolder.setText(str(currentFolder))
        btnFolder.doubleClick.connect(lambda: self.openFolder(str(currentFolder)))
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, btnFolder)

        btnChange = QPushButton()
        btnChange.setIcon(QIcon("iconChange.png"))
        btnChange.setIconSize(QSize(20, 20))
        btnChange.setStyleSheet(self.btnChangeStyle)
        btnChange.clicked.connect(self.openUpdateFolderForm)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 7, btnChange)

        btnClose = QPushButton()
        btnClose.setIcon(QIcon("iconClose.png"))
        btnClose.setIconSize(QSize(20, 20))
        btnClose.setStyleSheet(self.btnCloseStyle)
        btnClose.clicked.connect(lambda: self.DelFolder(self.tableWidget.cellWidget(self.tableWidget.currentRow(), 0).text()))
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 8, btnClose)


    def addRow(self, curentData):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        for i in range(6):
            self.tableWidget.setItem(self.tableWidget.rowCount() - 1, i, QtWidgets.QTableWidgetItem(str(curentData[i])))

        # self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).setTextAlignment(
        #     QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)

        self.setOpenBtn(6)
        self.setChangeBtn(7)
        self.setDelBtn(8)

    def openUpdateFolderForm(self):
        currentRow = self.tableWidget.currentRow()
        self.changeFolderWindow.currentRow = currentRow
        self.changeFolderWindow.newFolderName.setText(self.tableWidget.cellWidget(currentRow, 0).text())
        self.changeFolderWindow.setGeometry(self.geometry())
        self.changeFolderWindow.show()
        self.hide()


    def updateRow(self, curentData, curentRow):
        for i in range(6):
            self.tableWidget.setItem(curentRow, i, QtWidgets.QTableWidgetItem(str(curentData[i])))

    def openFolder(self, newFolder):

        if len(self.path) >= 2 and self.path[-2] == newFolder:
            self.path.pop()
        else:
            self.path.append(newFolder)
        if newFolder == "root":
            self.btnBack.setEnabled(False)
            self.path = ["root"]
        else:
            self.btnBack.setEnabled(True)


        self.currentFolder = newFolder
        allPath = ""
        for i in self.path:
            allPath += "/" + i

        self.folderLabel.setText("Текущая категория: " + allPath)
        self.data = []
        self.folders = []
        self.loadDB()
        self.loadTable()

    def fackGoBack(self):
        oldFolder = self.path[-2]
        self.openFolder(oldFolder)

    def setOpenBtn(self, i):
        btnOpen = QPushButton()
        btnOpen.setIcon(QIcon("iconOpen.png"))
        btnOpen.setIconSize(QSize(20, 20))
        btnOpen.setStyleSheet(self.btnOpenStyle)
        btnOpen.clicked.connect(self.openInfoForm)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, i, btnOpen)

    def setChangeBtn(self, i):
        btnChange = QPushButton()
        btnChange.setIcon(QIcon("iconChange.png"))
        btnChange.setIconSize(QSize(20, 20))
        btnChange.setStyleSheet(self.btnChangeStyle)
        btnChange.clicked.connect(self.openChangeForm)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, i, btnChange)

    def setDelBtn(self, i):
        btnClose = QPushButton()
        btnClose.setIcon(QIcon("iconClose.png"))
        btnClose.setIconSize(QSize(20, 20))
        btnClose.setStyleSheet(self.btnCloseStyle)
        btnClose.clicked.connect(self.Del)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, i, btnClose)

    def loadDB(self):
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()

        for row in cur.execute("SELECT * FROM FolderControl WHERE parentName = ?", (self.currentFolder,)):
            self.folders.append(row[0])

        for row in cur.execute("SELECT * FROM ItemControl WHERE folder = ?", (self.currentFolder,)):
            thisData = []
            for i in range(6):
                thisData.append(row[i])
            self.data.append(thisData)

    def fillUsedId(self):
        connection = sqlite3.connect("ItemDataBase.db")
        cur = connection.cursor()
        for row in cur.execute("SELECT id FROM ItemControl"):
            self.freeId.remove(row[0])

    def Del(self):
        button = QMessageBox.question(self, "Удаление данные", "Вы уверены?")
        if button == QMessageBox.StandardButton.Yes:
            connection = sqlite3.connect("ItemDataBase.db")
            cur = connection.cursor()
            cur.execute("SELECT * FROM ItemControl;")
            allMain = cur.fetchall()
            row = self.tableWidget.currentRow()
            # delIndex = self.tableWidget.currentRow()
            cur.execute("DELETE FROM ItemControl WHERE id = ?",
                        (self.tableWidget.item(row, 0).text(),))
            connection.commit()
            cur.execute("DELETE FROM TagsControl WHERE id = ?",
                        (self.tableWidget.item(row, 0).text(),))
            connection.commit()
            if row > -1:  # Если есть выделенная строка/элемент
                self.tableWidget.removeRow(row)
                self.tableWidget.selectionModel().clearCurrentIndex()

    def DelFolder(self, delName):
        print(delName)
        button = QMessageBox.question(self, "Удаление данные", "Вы уверены?")
        if button == QMessageBox.StandardButton.Yes:
            connection = sqlite3.connect("ItemDataBase.db")
            cur = connection.cursor()
            row = self.tableWidget.currentRow()
            cur.execute("DELETE FROM FolderControl WHERE name = ?", (delName,))
            connection.commit()
            for i in cur.execute("DELETE FROM FolderControl WHERE parentName = ?", (delName,)):
                self.DelFolder(i[0])
            connection.commit()
            # delId = cur.execute("SELECT id FROM ItemControl WHERE folder = ?", (delName,))
            cur.execute("DELETE FROM TagsControl WHERE TagsControl.id IN ( SELECT id FROM ItemControl WHERE folder = ? ) ",(delName,))
            connection.commit()
            cur.execute("DELETE FROM ItemControl WHERE folder = ?", (delName,))
            connection.commit()
            if row > -1:  # Если есть выделенная строка/элемент
                self.tableWidget.removeRow(row)
                self.tableWidget.selectionModel().clearCurrentIndex()