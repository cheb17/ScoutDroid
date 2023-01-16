import math
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
# from kivymd.tools.hotreload.app import MDApp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.graphics import Color, Ellipse
from kivy.properties import ObjectProperty, OptionProperty
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
import shutil
import os
import csv

from matplotlib.figure import Figure


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    pass


class Court(Image):
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    open('save_file.csv', 'w').write("Shot type,X,Y\n")
    # shots_made = 0
    # shots_missed = 0
    #
    # def on_touch_down(self, touch):
    #     d = 10
    #
    #     if self.collide_point(*touch.pos):
    #         self.canvas.add(Color(rgb=(46 / 255.0, 172 / 255.0, 88 / 255.0)))
    #         self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))
    #
    #         x = touch.x - self.pos[0]
    #         y = self.size[1] - touch.y + self.pos[1]  # modified line
    #
    #         # Don't write to the file if the touch event is a double tap
    #         if not touch.is_double_tap:
    #             with open('save_file.csv', 'a', newline='') as f:
    #                 print(f"Made,{x},{y}", file=f)
    #             # Increment the shots made counter
    #             self.shots_made += 1
    #
    #         if touch.is_double_tap:
    #             self.canvas.add(Color(rgb=(220 / 255.0, 8 / 255.0, 8 / 255.0)))
    #             d = 10
    #             self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))
    #             self.shots_missed += 1
    #             with open('save_file.csv', 'a', newline='') as f:
    #                 print(f"Missed,{x},{y}", file=f)
    #
    #         # Update the shooting percentage label
    #         self.parent.parent.ids.hi.text = \
    #             f"Shooting Percentage: {self.shots_made / (self.shots_made + self.shots_missed):.2f}"

    def on_touch_down(self, touch):
        d = 10
        if self.collide_point(*touch.pos):
            self.canvas.add(Color(rgb=(46 / 255.0, 172 / 255.0, 88 / 255.0)))
            self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))

            # Calculate the pixel location relative to the top-left corner of the image
            x = touch.x - self.pos[0]
            y = self.size[1] - touch.y + self.pos[1]  # modified line
            # print(f"Pixel location: ({x}, {y})")

            with open('save_file.csv', 'a', newline='') as f:
                print(f"Made,{x},{y}", file=f)

                if touch.is_double_tap:
                    self.canvas.add(Color(rgb=(220 / 255.0, 8 / 255.0, 8 / 255.0)))
                    d = 10
                    self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))
                    print(f"Missed,{x},{y}", file=f)

    def clear_drawing(self):
        self.canvas.clear()
        self.canvas.after.clear()
        open('save_file.csv', 'w').write("Shot type,X,Y\n")

    def save(self, path, filename):
        storage_path = os.environ['EXTERNAL_STORAGE']
        with open(os.path.join(storage_path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


class MainScreen(MDScreen):
    pass


class PlotScreen(MDScreen):
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize variables or load data here
        self.data = []

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        # storage_path = os.path.expanduser('~/sdcard')

        #external storage but only used in android phone
        # storage_path = os.environ['EXTERNAL_STORAGE']

        #stored in a private data
        shutil.move("save_file.csv", os.path.join(path, filename))
        self.dismiss_popup()

    def clear_drawing(self):
        self.ids.plotting.clear_drawing()


class VisualScreen(MDScreen):
    savefile = ObjectProperty(None)
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        # Open the file for reading from the JSON directory
        with open(os.path.join(path, 'json', filename[0]), 'r') as stream:
            # Create a reader object
            reader = csv.reader(stream)

            # Iterate through the rows of the file
            for row in reader:
                # Print each row
                print(row)
        #
        # self.dismiss_popup()

    # def load(self, path, filename):
    #     # Open the file for reading from internal storage
    #     with open(self.context.openFileInput(path, filename[0]), 'r') as stream:
    #         self.text_input.text = stream.read()
    #     # def load_csv(filename):
    #     #     with open(filename, 'r') as f:
    #     #         reader = csv.reader(f)
    #     #         data = list(reader)
    #     #     return data
    #     #
    #     # app = MDApp.get_running_app()  # Get the current instance of the App class
    #     # filename = app.user_data_dir + '/' + filename[0][0]
    #     # data = load_csv(filename)
    #     #
    #     # # Now you can use the 'data' list to access the contents of the CSV file
    #     # for row in data:
    #     #     print(row)
    #
    #     self.dismiss_popup()

    def show_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        # storage_path = os.environ['EXTERNAL_STORAGE']
        with open(os.path.join(path, filename), 'w') as stream:
            stream.write(self.text_input.text)

        self.dismiss_popup()


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    # _user_data_dir = ""
    media = OptionProperty('M', options=('XS', 'S', 'M', 'L', 'XL'))

    def build(self):
        Window.bind(size=self.update_media)
        Builder.load_file("app.kv")
        return WindowManager()

    def update_media(self, win, size):
        width, height = size
        self.media = (
            'XS' if width < 250 else
            'S' if width < 500 else
            'M' if width < 1000 else
            'L' if width < 1200 else
            'XL'
        )


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == "__main__":
    MyApp().run()