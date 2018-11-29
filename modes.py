""" Credit:
"Updated Animation Starter Code" template from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
Entry Box Tutorial: http://effbot.org/tkinterbook/entry.htm
Understanding .pack(): http://effbot.org/tkinterbook/pack.htm
Text Tutorials: https://www.tutorialspoint.com/python/tk_text.htm http://effbot.org/tkinterbook/text.htm
ScrollBat Tutorial: http://effbot.org/zone/tkinter-scrollbar-patterns.htm
Grid Tutorial: http://effbot.org/tkinterbook/grid.htm
Button Tutorial: http://effbot.org/tkinterbook/button.htm
Events and Binding Tutorial: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm

Credit: Got mode idea from https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html#modeDemo
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
    lineLen = data.width / 25
    lineHeight = data.width / 120
    leftCor = data.width / 40
    data.settingsIcon = SettingsIcon(lineLen, lineHeight, leftCor)
    data.chatLog = []
    data.overallEmotions = []
    data.userEntry = ""
    data.chatResponse = ""
   # trainEmotionDetector()

def mousePressed(event, data): 
    if data.mode == "start": 
        startMousePressed(event, data)
    elif data.mode == "settings":
        settingsMousePressed(event, data)
    elif data.mode == "run":
        runMousePressed(event, data)
    elif data.mode == "help":
        helpMousePressed(event, data)

def keyPressed(event, data): 
    if data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "settings":
        settingsKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
        
def timerFired(data, log): 
    if data.mode == "start":
        startTimerFired(data)
    elif data.mode == "settings":
        settingsTimerFired(data)
    elif data.mode == "run":
        runTimerFired(data, log)
    elif data.mode == "help":
        helpTimerFired(data)
        
def redrawAll(canvas, data, entry, scrollBar, log, button): 
    if data.mode == "start":
        log.grid_forget()
        entry.grid_forget()
        button.grid_forget()
        scrollBar.grid_forget()
        button.grid_forget()
        startRedrawAll(canvas, data)
    elif data.mode == "settings":
        log.grid_forget()
        entry.grid_forget()
        button.grid_forget()
        scrollBar.grid_forget()
        button.grid_forget()
        settingsRedrawAll(canvas, data)
    elif data.mode == "run":
        entry.grid(row = 2, columnspan = 6)
        canvas.grid(row = 0, columnspan = 8)
        scrollBar.grid(row = 1, column = 7)
        log.grid(row = 1, columnspan = 7)
        button.grid(row = 2, column = 6)
        runRedrawAll(canvas, data)
    elif data.mode == "help":
        helpRedrawAll(canvas, data)

###### start mode 
class ScreenButton(object):
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
    data.startButton = ScreenButton(data.width / 2, startY, buttonW, buttonH, "DodgerBlue1", "white", buttonFontSize, "Start")
    data.helpButton = ScreenButton(data.width / 2, helpY, buttonW, buttonH, "DodgerBlue1", "white", buttonFontSize, "Help")
    
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
# holds the current different message types
def messageType(data):
    greeting(data)
    question(data)
    farewell(data)

# chat responds to user entry
def chatBotResponse(data, log):
    data.userEntry.lower().strip()
    typicalResponse = ["ok", "nice", "sounds interesting"]
    data.chatResponse = random.choice(typicalResponse)
    messageType(data)
    log.insert(END, "\n" + data.chatResponse)

# chatbot processes the message said by user
def processMessage(data, log, entry):
    entry.delete(0, END)
    data.chatLog.append(data.userEntry)
    log.config(state = NORMAL)
    log.insert(END, "\n" + data.userEntry)
    chatBotResponse(data, log)
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    print(data.chatLog)
    
# when return key is pressed, submit message
def entryKeyPressed(event, data, entry, log):
    entryLog = entry.get()
    if event.keysym == "Return" and len(entryLog) > 0:
        data.userEntry = entryLog
        processMessage(data, log, entry)
        
# respond to different emotions
def respondToEmotion(emotion, log):
    msg = ""
    if emotion == "happy":
        happyResponses = ["I'm glad you're happy! That makes me happy too :)",
                        "Did something exciting happen? You seem happy!",
                        "Seeing you smile makes me smile too :)",
                        "You seem happy recently, by the way. Yay!"]
        msg = random.choice(happyResponses)
    elif emotion == "sad":
        sadResponses = ["You seem sad recently. What's up?",
                        "What's making you feel down, by the way?",
                        "I noticed that you seem sad. Want to talk about it?"]
        msg = random.choice(sadResponses)
    elif emotion == "angry":
        angryResponses = ["Ah! You seem kind of angry recently",
                        "You seem upset. What's wrong?"]
        msg = random.choice(angryResponses)
    elif emotion == "surprise":
        surpriseResponses = ["Did something happen? Why do you seem surprised?"
                            "What's new? You look surprised"]
        msg = random.choice(surpriseResponses)
    if len(msg) != 0:
        log.insert(END, "\n" + msg)
    
def sendMsg(data, log, entry):
    if len(entry.get()) > 0:
        data.userEntry = entry.get()
        processMessage(data, log, entry)
        
def runMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "settings"
        print("SETTINGS PRESSED")
    
def runKeyPressed(event, data):
    pass
    
def runTimerFired(data, log):
    pass
    # getEmotion()
    # # writes an overall emotion for every 10 emotions
    # if len(foundEmotions) == 10:
    #     overallEmotion = predictOverallEmotion(foundEmotions)
    #     data.overallEmotions.append(overallEmotion)
    #     del foundEmotions[:]
    # # when 10 overall emotions are found, check up on user
    # 
    # if len(data.overallEmotions) == 10:
    #     mainEmotion = predictOverallEmotion(data.overallEmotions)
    #     log.config(state = NORMAL)
    #     respondToEmotion(mainEmotion, log)
    #     data.overallEmotions = []
    #     log.yview_pickplace(END)
    #     log.config(state = DISABLED)
    # print("all emotions", data.overallEmotions)

        
def runRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "sky blue", width = 0)
    pixelLen = data.width / 30
    drawEyes(canvas, data, pixelLen)
    drawMouth(canvas, data, pixelLen)
    data.settingsIcon.color = "dark gray"
    data.settingsIcon.draw(canvas)
    
##### settings mode
def settingsMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "run"
        print("SETTINGS PRESSED")
    
def settingsKeyPressed(event, data):
    pass
    
def settingsTimerFired(data):
    pass
    
def settingsRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "gray", width = 0)
    data.settingsIcon.color = "white"
    data.settingsIcon.draw(canvas)

    
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
    def redrawAllWrapper(canvas, data, entry, scrollBar, log, button):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data, entry, scrollBar, log, button)
        canvas.update()

    def mousePressedWrapper(event, canvas, data, entry, scrollBar, log, button):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)

    def keyPressedWrapper(event, canvas, data, entry, scrollBar, log, button):
        keyPressed(event, data, entry, log)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)

    def timerFiredWrapper(canvas, data, entry, scrollBar, log, button):
        timerFired(data, log)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, entry, scrollBar, log, button)
        
    capture = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier("/Users/estherjang/Desktop/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    
    # sets up entry box for user message
    entry = Entry(root)
    entryWidth = data.width // 10
    entry.config(width = entryWidth)
    entry.grid(row = 2, columnspan = 6)
    
    # sets up scroll bar for the text log
    scrollBar = Scrollbar(root)
    
    # sets up the text log
    logWidth = data.width // 8
    logHeight = data.height // 100
    log = Text(root, width = logWidth, height = logHeight, yscrollcommand = scrollBar.set, state = DISABLED)
    scrollBar.config(command=log.yview)
    log.grid(row = 1, columnspan = 7)
    scrollBar.grid(row = 1, column = 7)
    
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.grid(row = 0, columnspan = 8)
    # handles button click
    def buttonCallback():
        sendMsg(data, log, entry)
    
    # sets up button to send message
    button = Button(root, text = "Send", command = buttonCallback)
    button.grid(row = 2, column = 6)
    # set up events, specify per widget type
    canvas.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, entry, scrollBar, log, button))
    canvas.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data, entry, scrollBar, log, button))
    entry.bind("<Key>", lambda event: entryKeyPressed(event, data, entry, log))
    timerFiredWrapper(canvas, data, entry, scrollBar, log, button)
    

    # and launch the app
    root.mainloop()  # blocks until window is closed
    capture.release()
    cv2.destroyAllWindows()

run(800, 500)