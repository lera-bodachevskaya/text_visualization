import shutil
import random
import sys
import os

from QtActivity.Qt5StartActivity import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GoogleImages import GoogleImages
from TextNN import TextNN
from Image import Image


class StartWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    autoSearch = 1
    imgNum = 5
    images = []
    index = 0

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menuButton.clicked.connect(self.menuClicked)
        self.ui.goButton.clicked.connect(self.goClicked)
        self.ui.nextButton.clicked.connect(self.nextClicked)
        self.ui.prevButton.clicked.connect(self.prevClicked)
        self.autoSearch = openFile()[0]
        self.imgNum = openFile()[1]

        print(self.autoSearch)
        print(self.imgNum)

    def goClicked(self):
        self.images = []
        text = self.ui.textEdit.toPlainText()
        if text != '':
            textNN = TextNN(text)
            keywords = textNN.findKeywords().split()

            if keywords[0] != 'food-safety':
                image = Image()
                images = image.GetImageFromDatabase(keywords)
                self.index = 0

                if len(images) > 1:
                    try:
                        images = images[1:int(self.imgNum) + 1]
                    except:
                        print('Not many pictures')

                    for i in images:
                        self.images.append(i[0])

                    random.shuffle(self.images)
                    path = self.images[self.index]
                    print(path)
                    self.showImage(path)
                else:
                    print("No picture")

                    if self.autoSearch == '0':
                        print("No auto search")
                        path = 'no_img.png'
                        self.showImage(path)
                    else:
                        print("Будем искать")
                        # self.img.source = 'C:\\Users\\Лерочка\\Desktop\\диплом\\Images\\wait.jpg'
                        self.images = self.imgSearch(keywords)
                        path = self.images[self.index]
                        self.showImage(path)
            else:
                QMessageBox.about(self, "Text Classification", "Bad text!")
        else:
            QMessageBox.about(self, "Text Classification", "Empty text!")

    def imgSearch(self, keywords):
        keywords = keywords[0]
        newImg = GoogleImages(keywords, self.imgNum)
        newImg.SearchImages()
        img = Image()
        files = os.listdir('source_images')
        img.images = []
        for f in files:
            img.CreateImageFromFile(f)
        res = []

        for i in img.images:
            i.tags = keywords
            src = 'source_images\\' + i.name
            to = 'tmp_images'
            shutil.move(src, to)
            i.url = to + i.name

        for i in img.images:
            res.append('tmp_images\\' + i.name)

        img.AddImagesToDatabaseWithTags()
        return res

    def nextClicked(self):
        text = self.ui.textEdit.toPlainText()
        if text != '':
            if self.index < len(self.images) - 1:
                self.index += 1
                path = self.images[self.index]
                self.showImage(path)
            else:
                print("out of range +")
        else:
            QMessageBox.about(self, "Text Classification", "Empty text!")

    def prevClicked(self):
        text = self.ui.textEdit.toPlainText()
        if text != '':
            if self.index > 0:
                self.index -= 1
                path = self.images[self.index]
                self.showImage(path)
            else:
                print("out of range -")
        else:
            QMessageBox.about(self, "Text Classification", "Empty text!")

    def showImage(self, path):
        pixmap = QPixmap(path)
        self.ui.imgLabel.setPixmap(pixmap)

    def menuClicked(self):
        self.close()


def openFile():
    f = open('settings.txt')
    params = f.read().split()
    f.close()
    return params


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = StartWindow()
    main.show()
    sys.exit(app.exec_())
