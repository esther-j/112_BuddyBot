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
    data.botColor = "LightBlue1"
    makeSettingsIcon(data)
    makeSettingsOptions(data)
    data.chatLog = []
    data.overallEmotions = []
    data.userEntry = ""
    data.colorOptions = ["LightBlue1", "red", "orange", "yellow", "green", "blue", "purple"]
    data.chatResponse = ""
    trainEmotionDetector()
    data.detectFace = True

def makeSettingsOptions(data):
    data.goHomeOption = SettingsOption(data.width / 6, data.height / 5, data.width / 30, "Go back home", "dark grey", data.height // 18)
    data.changeColorOption = SettingsOption(data.width / 6, data.height * 3 / 10, data.width / 30, "Change bot color", data.botColor, data.height // 18)
    data.faceDetectionOption = SettingsOption(data.width / 6, data.height * 2 / 5, data.width / 30, "Turn off face detection (currently on)", "dark grey", data.height // 18)

def makeSettingsIcon(data):
    lineLen = data.width / 25
    lineHeight = data.height / 90
    leftCor = data.width / 40
    data.settingsIcon = SettingsIcon(lineLen, lineHeight, leftCor)    

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
    elif data.mode == "run":
        runKeyPressed(event, data)
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
        
def makeButtons(data):
    startY = data.height * 9 / 20
    helpY = data.height * 3 / 5
    buttonW = data.width / 10
    buttonH = data.height / 20
    buttonFontSize = data.height // 18
    data.startButton = ScreenButton(data, data.width / 2, startY, "Start")
    data.helpButton = ScreenButton(data, data.width / 2, helpY, "Help")
    backX = data.width / 8
    backY = data.height / 10
    data.backButton = ScreenButton(data, backX, backY, "Back")
    
def startMousePressed(event, data):
    if data.startButton.isPressed(event.x, event.y):
        data.mode = "run"
    elif data.helpButton.isPressed(event.x, event.y):
        data.mode = "help"
        
def startKeyPressed(event, data):
    pass
    
def startTimerFired(data):
    cv2.destroyAllWindows()

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
    log.insert(END, "\nBuddyBot: %s" % data.chatResponse)

# chatbot processes the message said by user
def processMessage(data, log, entry):
    entry.delete(0, END)
    data.chatLog.append(data.userEntry)
    log.config(state = NORMAL)
    log.insert(END, "\nYou: %s" % data.userEntry)
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
    elif emotion == "surprised":
        surpriseResponses = ["Did something happen? Why do you seem surprised?"
                            "What's new? You look surprised"]
        msg = random.choice(surpriseResponses)
    if len(msg) != 0:
        log.insert(END, "\nBuddyBot: %s" % msg)
    
def sendMsg(data, log, entry):
    if len(entry.get()) > 0:
        data.userEntry = entry.get()
        processMessage(data, log, entry)
        
def runMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "settings"
    
def runKeyPressed(event, data):
    pass
    
def runTimerFired(data, log):
    cap = cv2.VideoCapture(0)
    print("detect face", data.detectFace)
    if data.detectFace:
        getEmotion()
        # writes an overall emotion for every 10 emotions
        if len(foundEmotions) == 10:
            overallEmotion = predictOverallEmotion(foundEmotions)
            data.overallEmotions.append(overallEmotion)
            del foundEmotions[:]
        # when 10 overall emotions are found, check up on user
        
        if len(data.overallEmotions) == 10:
            mainEmotion = predictOverallEmotion(data.overallEmotions)
            log.config(state = NORMAL)
            respondToEmotion(mainEmotion, log)
            data.overallEmotions = []
            log.yview_pickplace(END)
            log.config(state = DISABLED)
        print("all emotions", data.overallEmotions)
    else:
        cap.release()
        cv2.destroyAllWindows()

        
def runRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = data.botColor, width = 0)
    pixelLen = data.width / 30
    drawEyes(canvas, data, pixelLen)
    drawMouth(canvas, data, pixelLen)
    data.settingsIcon.color = "dark gray"
    data.settingsIcon.draw(canvas)
    
##### settings mode
def subtitle(data, canvas, topX, topY, title):
    size = data.height / 10    
    canvas.create_text(topX, topY, text = title, font = "arial %d bold" % size, anchor = NW)

def settingsMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "run"
    elif data.goHomeOption.isPressed(event.x, event.y):
        data.mode = "start"
    elif data.changeColorOption.isPressed(event.x, event.y):
        colorIndex = data.colorOptions.index(data.botColor)
        if colorIndex + 1 == len(data.colorOptions):
            newColor = 0
        else:
            newColor = colorIndex + 1
        data.botColor = data.colorOptions[newColor]
        data.changeColorOption.color = data.botColor
    elif data.faceDetectionOption.isPressed(event.x, event.y):
        if data.detectFace:
            data.detectFace = False
            data.faceDetectionOption.option = "Turn on face detection (currently off)"
        else:
            data.detectFace = True
            data.faceDetectionOption.option = "Turn off face detection (currently on)"            
    
def settingsKeyPressed(event, data):
    pass
    
def settingsTimerFired(data):
    cv2.destroyAllWindows()
    
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
    
def settingsRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "gray", width = 0)
    subtitle(data, canvas, data.width / 10, data.height / 120, "Settings")
    canvas.create_text(data.width * 7 / 20, data.height / 15, text = "(Click square to select/change)", font = "arial %d bold" % (data.height // 30), anchor = NW)
    data.settingsIcon.color = "white"
    data.settingsIcon.draw(canvas)
    data.goHomeOption.draw(canvas)
    data.changeColorOption.draw(canvas)
    data.faceDetectionOption.draw(canvas)

    
##### help mode
def helpMousePressed(event, data):
    if data.backButton.isPressed(event.x, event.y):
        data.mode = "start"
    
def helpKeyPressed(event, data):
    pass
    
def helpTimerFired(data):
    pass
    
def helpRedrawAll(canvas, data):
    data.backButton.draw(canvas)
    subtitle(data, canvas, data.width / 4, data.height / 20, "What is BuddyBot?")
    helpText = """\
    BuddyBot is a friendly, interactive chatbot who is always down to have a 
    conversation. BuddyBot can also detect emotions and wants to talk them out 
    with you. The bot is also customizable so you can personalize it however you
    want. This includes turning off face detection. 
    """
    canvas.create_text(0, data.height / 5, text = helpText, font = "arial 20", anchor = NW)
    
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

run(800, 500)
cv2.destroyAllWindows()
cap.release()