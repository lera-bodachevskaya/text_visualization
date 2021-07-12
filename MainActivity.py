import sys

from QtActivity.Qt5MainActivity import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from SettingsActivity import SettingsWindow
from ImageActivity import ImageWindow
from StartActivity import StartWindow
from TextActivity import TextWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    autoSearch = 1
    imgNum = 5

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.startButton.clicked.connect(self.startClicked)
        self.ui.textButton.clicked.connect(self.textClicked)
        self.ui.imageButton.clicked.connect(self.imageClicked)
        self.ui.settingsButton.clicked.connect(self.settingsClicked)

    def startClicked(self):
        self._new_window = StartWindow()
        self._new_window.show()

    def imageClicked(self):
        self._new_window = ImageWindow()
        self._new_window.show()

    def textClicked(self):
        self._new_window = TextWindow()
        self._new_window.show()

    def settingsClicked(self):
        self._new_window = SettingsWindow()
        self._new_window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
