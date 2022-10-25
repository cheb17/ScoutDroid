import kivy
import random
from PIL import Image, ImageDraw
import matplotlib.image as images
from kivy.graphics import Ellipse, Color
from matplotlib import pyplot as plt
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.behaviors import TouchBehavior

# data = images.imread('images/basketball_court.png')


class MainScreenPageApp(Screen):
    pass


class PlotScreenPageApp(Screen):
    def on_touch_down(self, touch):
        self.canvas.add(Color(rgb=(0, 255, 0)))
        d = 15
        self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))
        if touch.is_double_tap:
            self.canvas.add(Color(rgb=(1, 0, 0)))
            d = 15
            self.canvas.add(Ellipse(pos=(touch.x - d / 2, touch.y), size=(d, d)))


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("ScoutDroid.kv")


class ScoutDroidApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    ScoutDroidApp().run()
