#File Name: Main.py
import kivy
kivy.require("1.9.1")
from kivy.app import  App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('CustomWidgets/DraggingArea/draggingarea.kv')
Builder.load_file('CustomWidgets/BlocksMenu/menublocks.kv')

class MainGUI(BoxLayout):
    pass

class MainGUIApp(App):
    def build(self):
        return MainGUI()

if __name__ == '__main__':
    MainGUIApp().run()
