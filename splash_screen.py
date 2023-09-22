import os.path
import sqlite3
import sys
import time
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import main_window

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Экран загрузки')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)


        self.counter = 0
        self.n = 50 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(0)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40) # x, y
        self.labelTitle.setText('Сюда вставить название')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Если волк молчит то лучше его не перебивать</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('Загрузка...')



    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.2):
            self.labelDescription.setText('<strong>Паймон - лучший компаньон</strong>')
        elif self.counter == int(self.n * 0.4):
            self.labelDescription.setText('<strong>Тераформируем ландшафт</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Безумно можно быть первым ... </strong>')
        elif self.counter == int(self.n * 0.8):
            self.labelDescription.setText('<strong>Иногда жизнь — это жизнь, а ты в ней иногда</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            # time.sleep(1)

            self.myApp = main_window.App()
            self.myApp.show()

        self.counter += 1