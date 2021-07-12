import sys

from QtActivity.Qt5SettingsActivity import Ui_MainWindow
from PyQt5 import   QtWidgets
from PyQt5.QtWidgets import *

from AddModule import AddModule


class SettingsWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    autoSearch = 1
    imgNum = 5
    modelImageNN = 0
    fileName = ""

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.menuButton.clicked.connect(self.menuClicked)
        self.ui.addButton.clicked.connect(self.addClicked)
        self.ui.openButton.clicked.connect(self.openClicked)

        self.autoSearch = openFile()[0]
        self.imgNum = openFile()[1]
        self.modelImageNN = openFile()[2]

        self.ui.modulesTextEdit.setReadOnly(True)

        if self.autoSearch == '1':
            self.ui.searchCheckBox.setChecked(True)
        else:
            self.ui.searchCheckBox.setChecked(False)

        self.ui.numOfImg.setText(self.imgNum)
        self.ui.comboBox.setCurrentIndex(int(self.modelImageNN))

    def menuClicked(self):
        self.setParams()
        self.saveFile()
        self.close()

    def addClicked(self):
        if self.fileName != "":
            print("add")
            name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter module name:')

            if ok:
                if name != "":
                    AddModule(name, self.fileName)
                    QMessageBox.about(self, "Text Classification", "Ready!")
                else:
                    QMessageBox.about(self, "Text Classification", "Empty name!")
            else:
                print("ну передумал и передумал")
        else:
            QMessageBox.about(self, "Text Classification", "Empty path!")

    def openClicked(self):
        dialog = QFileDialog()
        self.fileName = dialog.getOpenFileName(filter="Text files (*.txt)")[0]
        self.ui.fileName.setText(self.fileName)

    def setParams(self):
        if self.ui.searchCheckBox.isChecked():
            self.autoSearch = 1
        else:
            self.autoSearch = 0

        self.imgNum = self.ui.numOfImg.text()
        self.modelImageNN = self.ui.comboBox.currentIndex()

    def saveFile(self):
        f = open('settings.txt', 'w')
        f.write(str(self.autoSearch) + '\n')
        f.write(str(self.imgNum) + '\n')
        f.write(str(self.modelImageNN))
        f.close()


def openFile():
    f = open('settings.txt')
    params = f.read().split()
    f.close()
    return params


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    main = SettingsWindow()
    main.show()
    sys.exit(app.exec_())
