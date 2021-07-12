from Database import Database
import os
import uuid

directory = 'source_images'
images = []


class Image:
    name, url, tags = '', '', ''
    images = []

    def __init__(self, name = '', url = '', tags = ''):
        self.name = name
        self.url = url
        self.tags = tags

    def PrintImage(self):
        print('name: ' + self.name + '\nurl: ' + self.url + '\ntags: ' + self.tags)

    def GetFilesFromDirectory(self):
        return os.listdir(directory)

    def CreateImageFromFile(self, fileName):
        url = directory + '\\' + fileName
        tags = ''
        img = Image(fileName, url, tags)
        images.append(img)
        self.images.append(img)

    def CreateImageFromDatabaseRecord(self, record):
        name = record[0]
        url = record[1]
        tags = ''
        img = Image(name, url, tags)
        images.append(img)

    def FillImages(self):
        files = self.GetFilesFromDirectory()
        for f in files:
            self.CreateImageFromFile(f)

    def AddImagesToDatabase(self):
        db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
        db.StartConnection()

        for img in images:
            values = [{'name': img.name}, {'url': img.url}]
            db.Insert('images', values)

        db.StopConnection()

    def AddImagesToDatabaseWithTags(self):
        db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
        db.StartConnection()

        for img in images:
            values = [{'name': img.name}, {'url': img.url}, {'tags': img.tags}]
            db.Insert('images', values)

        db.StopConnection()


    def AddOneImageToDatabaseWithTags(self, img):
        try:
            db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
            db.StartConnection()

            values = [{'name': img.name}, {'url': img.url}, {'tags': img.tags}]
            #db.Insert('images', values)

            db.StopConnection()
            return True
        except:
            return False

    def GetImageFromDatabase(self, keywords):
        db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
        db.StartConnection()
        img = db.ImageSelect('images', ['url'], keywords[0])
        db.StopConnection()
        return list(img)



    def GetAllImagesFromDatabase(self):
        db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
        db.StartConnection()
        tmp = db.Select('images', ['name', 'url'], [])
        res = []

        for elem in tmp:
            res.append(elem)

        del res[0]

        for elem in res:
            self.CreateImageFromDatabaseRecord(elem)

        db.StopConnection()
        return images

    def UpdateImageInDatabase(self):
        db = Database('images', 'postgres', 'qwerty', 'localhost', '5432')
        db.StartConnection()

        values = [{'tags': self.tags}]
        conditions = [{'url': self.url}]

        db.Update('images', values, conditions)
        db.StopConnection()