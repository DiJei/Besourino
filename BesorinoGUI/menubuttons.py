# File name: menubuttons.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from wifi import my_socket

class MenuBar(BoxLayout):
    def __init__(self,**kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.add_widget(Button(text='O'))
        self.add_widget(Button(text='S'))
        self.add_widget(Button(text='C',on_press=self.connect))
        self.add_widget(Button(text='P'))

    def connect(self,*args):
        my_socket.connect()
