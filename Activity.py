from kivy.core.window import Window
from kivy.app import App
import shutil
import os

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label

from GoogleImages import GoogleImages
from Database import Database
from TextNN import TextNN
from Manager import Manager
from Image import Image as ImageUser


class MyApp(App):
    textInput = TextInput(size_hint=(1, .18), halign='center', font_size=16)
    switch = Switch(size_hint=(.3, .3), active=True)
    switchText = Switch(size_hint=(.1, .1), active=True)
    img = Image(source="1.jpg")
    buttonSearch = Button(text='Start', size_hint=(.3, .3))
    switchValue = True
    images = []
    index = 1
    path = ""

    def build(self):
        Window.size = (800, 700)
        layout = BoxLayout(orientation='vertical', padding=(50, 5, 50, 50))
        # layout.add_widget(Label(text='Image & Text classification using AI', size_hint=(1, .5), font_size=20))
        layout.add_widget(Label(text='Image classification using AI', size_hint=(1, .5), font_size=18))
        layout.add_widget(self.textInput)

        layout2 = AnchorLayout(anchor_x='center')
        self.buttonSearch.bind(on_press=self.buttonPress)
        layout2.add_widget(self.buttonSearch)
        layout.add_widget(layout2)

        # layout3 = GridLayout(cols=3, padding=(0, 0, 0, 0), spacing=20)
        layout3 = BoxLayout(orientation='horizontal')
        layout3.add_widget(Button(text='<=', on_press=self.leftButtonPress, size_hint=(.1, 1)))
        layout3.add_widget(self.img)
        layout3.add_widget(Button(text='=>', on_press=self.rightButtonPress, size_hint=(.1, 1)))
        layout.add_widget(layout3)

        layout.add_widget(Label(text='Auto add', size_hint=(.3, .3), font_size=14))
        self.switch.bind(active=self.switch_callback)
        layout.add_widget(self.switch)
        return layout

    def switch_callback(self, switchObject, switchValue):
        self.switchValue = switchValue

    def buttonPress(self, instance):
        text = self.textInput.text
        if text:
            keywords = text
            manager = Manager(keywords)
            self.images = manager.images

            if len(self.images) > 1:
                self.index = 1
                path = self.images[self.index][0]
                self.img.source = path
            else:
                if not self.switchValue:
                    self.img.source = manager.path
                else:
                    print("Search..")
                    self.imgSearch(keywords)

    def rightButtonPress(self, instance):
        text = self.textInput.text
        if text:

            if self.index < len(self.images) - 1:
                self.index += 1
                path = self.images[self.index][0]
                self.img.source = path
            else:
                print("out of range +")

    def leftButtonPress(self, instance):
        text = self.textInput.text
        if text:
            if self.index > 1:
                self.index -= 1
                path = self.images[self.index][0]
                self.img.source = path
            else:
                print("out of range -")

    def imgSearch(self, text):
        newImg = GoogleImages(text, 5)
        newImg.SearchImages()
        img = ImageUser()
        files = os.listdir('source_images')
        img.images = []
        for f in files:
            img.CreateImageFromFile(f)

        keywords = text
        for i in img.images:
            i.tags = keywords
            src = 'source_images\\' + i.name
            to = 'tmp_images'
            shutil.move(src, to)
            i.url = to + i.name
        img.AddImagesToDatabaseWithTags()
        print("Ok")


if __name__ == "__main__":
    MyApp().run()
