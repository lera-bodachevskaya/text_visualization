import sys

from QtActivity.Qt5ImageActivity import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from ImageNN import ImageNN
from Image import Image


class ImageWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    fileName = ''
    modelImageNN = 0

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.openButton.clicked.connect(self.openClicked)
        self.ui.databaseButton.clicked.connect(self.databaseClicked)
        self.ui.goButton.clicked.connect(self.goClicked)
        self.ui.textEdit.setReadOnly(True)
        self.ui.tagsEdit.setReadOnly(True)

        self.modelImageNN = openFile()[2]
        print(self.modelImageNN)

    def databaseClicked(self):

        if self.fileName != '':
            name = self.fileName.split('/')
            name = name[len(name) - 1]

            tags = self.ui.tagsEdit.toPlainText().split()

            if len(tags) > 0:
                res = ''
                for elem in tags:
                    res += elem + ' '

                img = Image(name, self.fileName, res)
                img.PrintImage()
                isOk = False
                isOk = img.AddOneImageToDatabaseWithTags(img)

                if isOk:
                    QMessageBox.about(self, "Add to Database", "Successful Insert")
                else:
                    QMessageBox.about(self, "Add to Database", "Insert Error")
            else:
                QMessageBox.about(self, "Image Classification", "Empty tags!")

        else:
            QMessageBox.about(self, "Image Classification", "Empty file name!")

    def openClicked(self):
        self.fileName = QFileDialog.getOpenFileName()[0]
        self.ui.textEdit.setText(self.fileName)

    def goClicked(self):
        if self.fileName != '':
            imgNN = ImageNN(str(self.modelImageNN))
            tags = imgNN.PredictingObjectClassByUrl(self.fileName)
            self.ui.tagsEdit.setText(tags)
        else:
            QMessageBox.about(self, "Image Classification", "Empty file name!")

    def menuClicked(self):
        self.close()


def openFile():
    f = open('settings.txt')
    params = f.read().split()
    f.close()
    return params


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = ImageWindow()
    main.show()
    sys.exit(app.exec_())
