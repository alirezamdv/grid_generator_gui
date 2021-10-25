"""
alireza.mahdavi@awi.de
a.mahdavi@outlook.com
"""
import sys
from PyQt5.QtWidgets import QApplication

from src.main import MapWindow
from src import StartDialog

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWindow()
    sys.exit(app.exec_())