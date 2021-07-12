import fasttext


class TextNN:
    model = fasttext.load_model("models/text_model.bin")
    text = ""

    def __init__(self, text):
        self.text = text

    def findKeywords(self):
        keyword = self.model.predict(self.text)[0][0].replace("__label__", "")
        print("Ключевые слова: " + keyword)
        return keyword
