# ЧТОБІ СДЕЛАТЬ ui.py: python -m PyQt5.uic.pyuic -x untitled.ui -o ui.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

app = QApplication([])
ex = Widget()

ex.show()
app.exec_()
