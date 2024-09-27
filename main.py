import sys
from PyQt5.QtWidgets import *
from databaseconnection import DatabaseConnection
from window import Window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mydbconnection = DatabaseConnection()
    window = Window(mydbconnection)
    window.show()
    sys.exit(app.exec_())