import fasttext


class AddModule:
    text, trainSet = "", ""
    model = None

    def __init__(self, name, trainSet):
        self.name = name
        self.trainSet = trainSet
        self.CreateModel()

    def CreateModel(self):
        self.model = fasttext.train_supervised(self.trainSet)
        self.SaveModel()

    def SaveModel(self):
        self.model.save_model('models' + self.name + ".bin")

