#### # Widgets
### Sets up the different personlized widgets
### Widgets include buttons, settings options, subtitles, and settings icon

from tkinter import *

# method to write a subtitle
def subtitle(data, canvas, topX, topY, title):
    size = data.height / 10    
    canvas.create_text(topX, topY, text = title, font = "arial %d bold" % size, anchor = NW)

# method to create a screen button
class ScreenButton(object):
    def __init__(self, data, cx, cy, text):
        self.cx = cx
        self.cy = cy
        self.width = data.width / 10
        self.height = data.height / 20
        self.color = "DodgerBlue1"
        self.fontColor = "white"
        self.size = data.height // 18
        self.text = text
        
    def draw(self, canvas):
        canvas.create_rectangle(self.cx - self.width, self.cy - self.height, self.cx + self.width, self.cy + self.height, fill = self.color, width = 0)
        canvas.create_text(self.cx, self.cy, text = self.text, fill = self.fontColor, font = "arial %s" % self.size)

    def isPressed(self, mouseX, mouseY):
        leftX = self.cx - self.width
        rightX = self.cx + self.width
        upY = self.cy - self.height
        downY = self.cy + self.height
        if mouseX >= leftX and mouseX <= rightX:
            if mouseY >= upY and mouseY <= downY:
                return True
        return False
        
class SettingsOption(object):
    def __init__(self, x, y, boxLen, option, color, size):
        self.x = x
        self.y = y
        self.option = option
        self.color = color
        self.boxLen = boxLen
        self.size = size
        
    def draw(self, canvas):
        canvas.create_rectangle(self.x - 2 * self.boxLen, self.y, self.x - self.boxLen, self.y + self.boxLen, fill = self.color)
        canvas.create_text(self.x, self.y, text = self.option, font = "arial %d" % self.size, anchor = NW)
    
    def isPressed(self, mouseX, mouseY):
        if mouseX >= self.x - 2 * self.boxLen and mouseX <= self.x - self.boxLen:
            if mouseY >= self.y and mouseY <= self.y + self.boxLen:
                return True
        return False

# method to create a settings icon
class SettingsIcon(object):
    def __init__(self, len, height, leftCoordinate):
        self.color = "gray"
        self.len = len
        self.height = height
        self.coord = leftCoordinate
        
    def draw(self, canvas):
        for i in range(3):
            canvas.create_rectangle(self.coord, self.coord + 2 * i * self.height, self.coord + self.len, self.coord + self.height + 2 * i * self.height, fill = self.color, width = 0)
            
    def isPressed(self, mouseX, mouseY):
        if mouseX >= self.coord and mouseX <= self.coord + self.len:
            if mouseY >= self.coord and mouseY <= self.coord + (self.height * 5):
                return True
        return False