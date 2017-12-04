# File name: draggingblock.py
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from random import randrange
from wifi import my_socket

play_sound_fail = SoundLoader.load('sounds/start_fail.wav')
play_sound_succes = SoundLoader.load('sounds/start_succes.wav')
connect_sound = SoundLoader.load('sounds/connect.mp3')
click_sound = SoundLoader.load('sounds/touch.wav')
erase_sound = SoundLoader.load('sounds/erase.wav')


"""
    DragBlock Class:
    Represent the behave of a common dragging blocks, like
    connection between other blocks.
"""
class DragBlock(RelativeLayout):
    type = ""
    id = 0
    command_list = []
    def __init__(self,type,id,source_photo,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        self.left_block = None
        self.right_block = None
        self.id = id
        self.type = type
        self.command_list = [self.id]
        self.bind(pos=self.update)
        self.bind(size=self.update)
        with self.canvas:
            self.rect = Rectangle(source=source_photo, pos=self.pos, size=self.size)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.left_block is not None:
                self.left_block.right_block = None
                self.left_block.unbind()
            self.left_block = None
            self.selected = True
            click_sound.play()
            return True

    def on_touch_move(self, touch):
        if self.selected:
            self.center = (touch.x,touch.y)
            return True

    def on_touch_up(self, touch):
        if self.selected:
            menu_block = self.parent.block_menu
            #Delete the DragBlock
            if menu_block.collide_point(touch.x, touch.y):
                self.eraseBlocks()
                erase_sound.play()
                return True
            #Connect Blocks
            left_block = False
            for block in self.parent.children:
                if block is not self:
                    if self.checkRight(block,touch) and block.left_block == None:
                        block.left_block = self
                        self.right_block = block
                        self.pos = block.x - block.width*0.77, block.y
                        self.right_block.left_block.bind(pos=self.right_block.updatePosLeftBlock)
                        connect_sound.play()
                    elif self.checkLeft(block, touch) and block.right_block == None:
                        self.left_block = block
                        block.right_block = self
                        self.pos = self.left_block.x + self.left_block.width*0.77, self.left_block.y
                        self.left_block.bind(pos=self.updatePosLeftBlock)
                        left_block = True
                        connect_sound.play()
                    elif block.left_block is not None:
                        block.center = (block.left_block.center_x + block.left_block.width*0.77,block.left_block.center_y)
            if left_block is not True:
                if self.left_block is not None:
                    self.left_block.unbind()
                    self.left_block = None
            self.selected = False
            return True
        #Return default event for upper class
        return RelativeLayout.on_touch_up(self, touch)

    def update(self, *args):
        self.rect.size = (self.size)

    def updatePosLeftBlock(self, *args):
        if  self.left_block is not None:
            self.pos = self.left_block.x + self.left_block.width*0.77, self.left_block.y

    def updatePosRightBlock(self, *args):
        if  self.right_block is not None:
            self.right_block.pos = self.x + self.width*0.77, self.y

    def checkLeft(self,block,touch):
        if self.x > block.x + (block.width/2) and self.x < block.x  + block.width and self.y >= block.y*0.95 and self.y <= block.y + block.height:
            return True

    def checkRight(self,block,touch):
        if block.id == "0" or (block.id == "1" and block.type == "F"):
            return False
        if self.x + self.width > block.x  and self.x + self.width < block.x + (block.width/2) and self.y >= block.y*0.95  and self.y <= block.y + block.height:
            return True

    def eraseBlocks(self):
        temp = None
        end = self
        while(end.right_block != None):
            end = end.right_block
        while(end != self):
            temp = end
            end = temp.left_block
            self.parent.remove_widget(temp)
        self.parent.remove_widget(self)

"""
    DragMacroBlock Class:
    Combination fo due blocks when one is
"""
class DragMacroBlock(DragBlock):
    type = ""
    id = 0
    command_list = []
    def __init__(self,type,id,source_photo,**kwargs):
        super(DragBlock, self).__init__(**kwargs)
        self.selected = True
        self.left_block = None
        self.right_block = None
        self.id = id
        self.type = type
        self.command_list = [self.id]
        self.bind(pos=self.update)
        self.bind(size=self.update)
        self.bind()
        self.color  = "[color="
        self.color  += hex(randrange(20,255,10))[2:]
        self.color  += hex(randrange(20,255,10))[2:]
        self.color  += hex(randrange(20,255,10))[2:]
        self.color  += "]"
        self.sign = Label(text =  self.color +"#",markup = True)
        self.sign.font_size = str(self.size[0]*0.65) + "sp"
        self.sign.texture_update()
        with self.canvas:
            self.rect = Rectangle(source=source_photo, pos=self.pos, size=self.size)
        self.add_widget(self.sign)

    def buildCommands(self):
        self.command_list = []
        temp = self.right_block
        while (temp is not None):
            if temp.type == 'M':
                 command = "M" + str(temp.id)
                 id = temp.id
                 times = 1
                 if int(temp.id) <= 4:
                     while(True):
                         temp = temp.right_block
                         if (temp is not None):
                             if (temp.type == "M" and temp.id == id):
                                 times += 1
                             else:
                                 break
                         else:
                             break
                     if times < 10:
                         command += ("0" + str(times))
                     else:
                         command += str(times)
                     self.command_list = self.command_list + [command]
                 else:
                    self.command_list = self.command_list + [command]
                    temp = temp.right_block
            elif temp.type == 'A':
                 command = "A" + str(temp.id)
                 id = temp.id
                 times = 1
                 if int(temp.id) <= 8:
                     while(True):
                         temp = temp.right_block
                         if (temp is not None):
                             if (temp.type == "A" and temp.id == id):
                                 times += 1
                             else:
                                 break
                         else:
                             break
                     if times < 10:
                         command += ("0" + str(times))
                     else:
                         command += str(times)
                     self.command_list = self.command_list + [command]
                 else:
                    self.command_list = self.command_list + [command]
                    temp = temp.right_block
            elif temp.type == 'S':
                command = "S" + str(temp.id)
                id = temp.id
                self.command_list = self.command_list + [command]
                temp = temp.right_block
            elif temp.type == 'F' and temp.id == "2" and temp.mainBrick != self:
                command_list = temp.get_command_list()
                for item in command_list:
                    self.command_list = self.command_list + [item]
                temp = temp.right_block
            else:
                 temp = temp.right_block
        return self.command_list

    def checkLeft(self,block,touch):
        return False


"""
    DragActorMacroBlock Class:

"""
class DragActorMacroBlock(DragBlock):
    type = ""
    id = 0
    command_list = []
    mainBrick = None
    label = None

    def checkLeft(self,block,touch):
        if self.x > block.x + (block.width/2) and self.x < block.x  + block.width and self.y >= block.y*0.95 and self.y <= block.y + block.height:
            if block.type == "F" and block.id == "1":
                self.mainBrick = block
                if self.label:
                    self.remove_widget(self.label)
                self.label = Label(text=  block.color +"#",markup = True)
                self.label.font_size = str(self.size[0]*0.65) + "sp"
                self.label.texture_update()
                if len(self.children) == 0:
                    self.add_widget(self.label)
            return True

    def get_command_list(self):
        if self.mainBrick is not None:
            return self.mainBrick.buildCommands()

"""
    DragPlayButton Class:
    Have all behaves of a commun dragging block but this on
    act as a button as well to transmit commands to robot
"""
class DragPlayButton(DragBlock):
    command_list = []
    data_list = []

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            if self.checkCenter(touch):
                self.sendCommands()
            if self.left_block is not None:
                self.left_block.command_list = [self.left_block.id]
            self.left_block = None
            self.selected = True
            return True

    def checkLeft(self,block,touch):
        return False

    def buildCommands(self):
        self.command_list = []
        temp = self
        self.command_list = self.command_list + [temp.id]
        temp = temp.right_block
        while (temp is not None):
            if temp.type == 'M':
                 command = "M" + str(temp.id)
                 id = temp.id
                 times = 1
                 if int(temp.id) <= 4:
                     while(True):
                         temp = temp.right_block
                         if (temp is not None):
                             if (temp.type == "M" and temp.id == id):
                                 times += 1
                             else:
                                 break
                         else:
                             break
                     if times < 10:
                         command += ("0" + str(times))
                     else:
                         command += str(times)
                     self.command_list = self.command_list + [command]
                 else:
                    self.command_list = self.command_list + [command]
                    temp = temp.right_block
            elif temp.type == 'A':
                 command = "A" + str(temp.id)
                 id = temp.id
                 times = 1
                 if int(temp.id) <= 8:
                     while(True):
                         temp = temp.right_block
                         if (temp is not None):
                             if (temp.type == "A" and temp.id == id):
                                 times += 1
                             else:
                                 break
                         else:
                             break
                     if times < 10:
                         command += ("0" + str(times))
                     else:
                         command += str(times)
                     self.command_list = self.command_list + [command]
                 else:
                    self.command_list = self.command_list + [command]
                    temp = temp.right_block
            elif temp.type == 'S':
                command = "S" + str(temp.id)
                id = temp.id
                self.command_list = self.command_list + [command]
                temp = temp.right_block
            elif temp.type == 'F' and temp.id == "2":
                command_list = temp.get_command_list()
                for item in command_list:
                    self.command_list = self.command_list + [item]
                temp = temp.right_block

            else:
                 temp = temp.right_block

    def sendCommands(self):
        self.buildCommands()
        my_socket.connect()
        self.data_list = self.command_list[1:]
        msg = ""
        for x in self.data_list:
            msg += str(x)
        if my_socket.send_data(msg):
            play_sound_succes.play()
        else:
            play_sound_fail.play()

    def checkCenter(self,touch):
        if touch.x > self.x + self.width*0.70 or touch.x < self.x + self.width*0.30:
            return False
        if touch.y > self.y + self.height*0.70 or touch.y < self.y + self.height*0.30:
            return False
        return True
