# File name: menublocks.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from draggingblock import DragBlock
from draggingblock import DragPlayButton
from draggingblock import DragMacroBlock
from draggingblock import DragActorMacroBlock
from kivy.core.audio import SoundLoader
import json

click_sound = SoundLoader.load('sounds/touch.wav')

#Tab
class BlocksMenu(TabbedPanel):
    def __init__(self, **kwargs):
        super(BlocksMenu,self).__init__(**kwargs)
        self.buildTab()

    def buildTab(self):
        self.background_image = "images/gui_elements/tab_darkblue.png"
        with open("config/blocks.json") as json_data:
            blocks_config = json.load(json_data)
            for tab in blocks_config["tabs"]:
                #newTab = TabbedPanelItem(text = str(tab["id"]))
                block_type = str(tab["id"])[0]
                newTab = TabbedPanelItem()
                color_tab = []
                for color in tab["rgba"]:
                    color_tab.append(color)
                newTab.background_color = color_tab
                newLayout = StackLayout(spacing = 10)
                for block in tab["blocks"]:
                    newBlock = Block(block_type,str(block["id"]),str(block["source"]))
                    newLayout.add_widget(newBlock)
                newTab.content = newLayout
                self.add_widget(newTab)


class Block(RelativeLayout):
    def __init__(self,type,id,source_image,**kwargs):
        super(Block,self).__init__(**kwargs)
        self.blockType = type
        self.blockID = id
        self.source_image = source_image
        self.da = None
        self.bind(pos=self.update)
        self.bind(size=self.update)
        with self.canvas:
            self.rect = Rectangle(size = self.size, source = self.source_image)


    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.da = self.parent.parent.parent.drawing_area
            (x,y) = self.da.to_widget(touch.x, touch.y)
            if self.blockType == "M" or self.blockType == "S"  or self.blockType == "A":
                self.draw(self.da, x, y,self.blockType,self.blockID,self.source_image)
            elif self.blockType == "F" and  self.blockID == "1":
                self.drawMacroBlock(self.da, x, y,self.blockType,self.blockID,self.source_image)
            elif self.blockType == "F" and  self.blockID == "2":
                self.draw(self.da, x, y,self.blockType,self.blockID,self.source_image)
            else:
                self.drawPlay(self.da, x, y,self.blockID,self.source_image)
            click_sound.play()
            return True
        return super(Block,self).on_touch_down(touch)

    def update(self, *args):
        self.size = (self.parent.height,self.parent.height)
        self.rect.size = (self.parent.height,self.parent.height)

    def draw(self, da, x, y,type,id,source):
        if (type == "F" and id == "2"):
            db = DragActorMacroBlock(type,id,source)
        else:
            db = DragBlock(type,id,source)
        db.center = (x,y)
        da.add_widget(db)
        da.children = da.children[::-1]

    def drawPlay(self, da, x, y,id,source):
        db = DragPlayButton("-",id,source)
        db.center = (x,y)
        da.add_widget(db)
        da.children = da.children[::-1]

    def drawMacroBlock(self, da, x, y,type,id,source):
        db = DragMacroBlock(type,id,source)
        db.center = (x,y)
        da.add_widget(db)
        da.children = da.children[::-1]
