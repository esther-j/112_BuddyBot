""" Credit: Got mode idea from https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html#modeDemo
Credit got colors from: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter"""

# major work in progress :)

from emotionReader import *
from tkinter import *
import time
from drawChatbot import *
from chatbotAnswer import *
from tkinter import *
import random
import cv2
import numpy as np


def init(data): 
    data.mode = "start" 
    makeButtons(data)
    data.chatLog = []
    data.overallEmotions = []
    data.userEntry = ""
    data.chatResponse = ""

def mousePressed(event, data): 
    if data.mode == "load":
        loadMousePressed(event, data)
    elif data.mode == "start": 
        startMousePressed(event, data)
    elif data.mode == "settings":
        settingsMousePressed(event, data)
    elif data.mode == "run":
        runMousePressed(event, data)
    elif data.mode == "help":
        helpMousePressed(event, data)

def keyPressed(event, data): 
    if data.mode == "load":
        loadKeyPressed(event, data)
    elif data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "settings":
        settingsKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
        
def timerFired(data): 
    if data.mode == "load":
        loadTimerFired(data)
    elif data.mode == "start":
        startTimerFired(data)
    elif data.mode == "settings":
        settingsTimerFired(data)
    elif data.mode == "run":
        runTimerFired(data)
    elif data.mode == "help":
        helpTimerFired(data)
        
def redrawAll(canvas, data): 
    if data.mode == "load":
        loadRedrawAll(canvas, data)
    elif data.mode == "start":
        startRedrawAll(canvas, data)
    elif data.mode == "settings":
        settingsRedrawAll(canvas, data)
    elif data.mode == "run":
        runRedrawAll(canvas, data)
    elif data.mode == "help":
        helpRedrawAll(canvas, data)
        
##### load mode
def loadMousePressed(event, data):
    pass
    
def loadKeyPressed(event, data):
    pass

def loadTimerFired(data):
    pass

def loadRedrawAll(canvas, data):
    startTime = time.time()
    trainEmotionDetector()
    stopTime = time.time()
    print(stopTime - startTime)
    data.mode = "start"

###### start mode 
class Button(object):
    def __init__(self, cx, cy, width, height, color, fontColor, size, text):
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.color = color
        self.fontColor = fontColor
        self.size = size
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
        
def makeButtons(data):
    startY = data.height * 9 / 20
    helpY = data.height * 3 / 5
    buttonW = data.width / 10
    buttonH = data.height / 20
    buttonFontSize = data.height // 18
    data.startButton = Button(data.width / 2, startY, buttonW, buttonH, "DodgerBlue1", "white", buttonFontSize, "Start")
    data.helpButton = Button(data.width / 2, helpY, buttonW, buttonH, "DodgerBlue1", "white", buttonFontSize, "Help")
    
def startMousePressed(event, data):
    if data.startButton.isPressed(event.x, event.y):
        print("START PRESSED")
        data.mode = "run"
        
    elif data.helpButton.isPressed(event.x, event.y):
        print("HELP PRESSED")
        # data.mode = "help"
        
def startKeyPressed(event, data):
    pass
    
def startTimerFired(data):
    pass    

def startRedrawAll(canvas, data):
    titleFontSize = data.height // 6

    canvas.create_rectangle(0, 0, data.width, data.height, fill = "LightBlue1", width = 0)
    canvas.create_text(data.width / 2, data.height / 4, text = "BuddyBot", fill = "DeepSkyBlue2", font = "arial %d bold" % titleFontSize)
    data.startButton.draw(canvas)
    data.helpButton.draw(canvas)
    
##### run chatbot mode
def runMousePressed(event, data):
    pass
    
def runKeyPressed(event, data):
    pass
    
def runTimerFired(data):
    pass
    
def runRedrawAll(canvas, data):
    pass
    
##### settings mode
def settingsMousePressed(event, data):
    pass
    
def settingsKeyPressed(event, data):
    pass
    
def settingsTimerFired(data):
    pass
    
def settingsRedrawAll(canvas, data):
    pass
    
##### help mode
def helpMousePressed(event, data):
    pass
    
def helpKeyPressed(event, data):
    pass
    
def helpTimerFired(data):
    pass
    
def helpRedrawAll(canvas, data):
    pass
    
    #################################### # use the run function as-is #################################### 
def run(width=300, height=300): 
    def redrawAllWrapper(canvas, data): 
        canvas.delete(ALL) 
        canvas.create_rectangle(0, 0, data.width, data.height, fill='white', width=0) 
        redrawAll(canvas, data) 
        canvas.update() 
        
    def mousePressedWrapper(event, canvas, data): 
        mousePressed(event, data) 
        redrawAllWrapper(canvas, data) 
        
    def keyPressedWrapper(event, canvas, data): 
        keyPressed(event, data) 
        redrawAllWrapper(canvas, data) 
        
    def timerFiredWrapper(canvas, data): 
        timerFired(data) 
        redrawAllWrapper(canvas, data) 
        
    # pause, then call timerFired again 
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data) 
    # Set up data and call init 
    class Struct(object): 
        pass 
    data = Struct() 
    data.width = width 
    data.height = height 
    data.timerDelay = 100 # milliseconds 
    root = Tk() 
    root.resizable(width=False, height=False) # prevents resizing window 
    init(data) # create the root and the canvas 
    canvas = Canvas(root, width=data.width, height=data.height)     
    canvas.configure(bd=0, highlightthickness=0) 
    canvas.pack() # set up events      
    root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, data)) 
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, data)) 
    timerFiredWrapper(canvas, data) # and launch the app 
    root.mainloop() # blocks until window is closed 
    
run(800, 500)