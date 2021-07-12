from Database import Database
from Image import Image
from ImageNN import ImageNN
import pandas as pd


class Manager:
    text = ""
    keywords = []
    image = Image()
    path = ""
    images = []

    def __init__(self, text):
        self.text = text
        self.findKeywords()
        self.findImage()

    def findKeywords(self):
        self.keywords = self.text.split()

    def findImage(self):
        self.images = self.image.GetImageFromDatabase(self.keywords)

        if len(self.images) > 1:
            self.path = self.images[1][0]
        else:
            self.path = 'no_img.jpg'
            print("No picture")

