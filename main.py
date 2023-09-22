import os.path
import sqlite3
import sys
import time
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import splash_screen

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyleSheet('''

            #LabelTitle {
                font-size: 60px;
                color: #93deed;
            }

            #LabelDesc {
                font-size: 30px;
                color: #c2ced1;
            }

            #Fon{
                border-radius: 10px;
            }

            #LabelLoading {
                font-size: 30px;
                color: #e8e8eb;
            }

            QFrame {
                color: rgb(220, 220, 220);
                border-radius: 10px;
            }

            QProgressBar {
                background-color: #DA7B93;
                color: rgb(200, 200, 200);
                border-style: none;
                border-radius: 10px;
                text-align: center;
                font-size: 30px;
            }

            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
            }
        ''')

    splash = splash_screen.SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')