import sys

from QtActivity.Qt5TextActivity import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from TextNN import TextNN


class TextWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.goButton.clicked.connect(self.goClicked)

        self.ui.tagsEdit.setReadOnly(True)

    def goClicked(self):
        text = self.ui.textEdit.toPlainText()
        if text != '':
            textNN = TextNN(text)
            keywords = textNN.findKeywords()
            self.ui.tagsEdit.setText(keywords)
        else:
            QMessageBox.about(self, "Text Classification", "Empty text!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = TextWindow()
    main.show()
    sys.exit(app.exec_())
