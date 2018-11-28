""" Credit:
"Updated Animation Starter Code" template from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
Entry Box Tutorial: http://effbot.org/tkinterbook/entry.htm
Understanding .pack(): http://effbot.org/tkinterbook/pack.htm
Text Tutorials: https://www.tutorialspoint.com/python/tk_text.htm http://effbot.org/tkinterbook/text.htm
ScrollBat Tutorial: http://effbot.org/zone/tkinter-scrollbar-patterns.htm
Grid Tutorial: http://effbot.org/tkinterbook/grid.htm
Button Tutorial: http://effbot.org/tkinterbook/button.htm
Events and Binding Tutorial: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
"""

"""Credits for openCV tutorials:
Live camera capture: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html#display-video
Face detection: https://docs.opencv.org/3.4.3/d7/d8b/tutorial_py_face_detection.html
"""

from drawChatbot import *
from emotionReader import *
from chatbotAnswer import *
from tkinter import *
import random
import cv2
import numpy as np

####################################
# customize these functions
####################################
# initalizes the chat data
def init(data):
    data.chatLog = []
    data.overallEmotions = []
    data.userEntry = ""
    data.chatResponse = ""
    data.foundFace = False
    data.foundFirstFace = False

# if the mouse is pressed, bot should say ouch (some binding problems)
def mousePressed(event, data, log):
    log.config(state = NORMAL)
    log.insert(END, "\n" + "ouch!")
    log.yview_pickplace(END)
    log.config(state = DISABLED)

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

# chatbot processes that it has found a face
def processFace(data, log):
    faceDetection = "I found your face!"
    log.config(state = NORMAL)
    if data.foundFace and not data.foundFirstFace:
        data.chatLog.append(faceDetection)
        data.foundFirstFace = True
        log.insert(END, "\n" + faceDetection)    
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    print(data.chatLog)
        
# key press for canvas - currently inactive
def keyPressed(event, data, entry, log):
    pass
    
# when return key is pressed, submit message
def entryKeyPressed(event, data, entry, log):
    entryLog = entry.get()
    if event.keysym == "Return" and len(entryLog) > 0:
        data.userEntry = entryLog
        processMessage(data, log, entry)

# timer fire -> necessary for typical bot movement
def timerFired(data, log):
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
        log.insert(END, "\n" + "you seem %s recently. what's up?" % mainEmotion)
        data.overallEmotions = []
        log.yview_pickplace(END)
        log.config(state = DISABLED)
    print("all emotions", data.overallEmotions)
        

# draw bot in canvas
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "sky blue", width = 0)
    pixelLen = data.width / 30
    drawEyes(canvas, data, pixelLen)
    drawMouth(canvas, data, pixelLen)
    drawSettings(canvas, data)
        
def sendMsg(data, log, entry):
    if len(entry.get()) > 0:
        data.userEntry = entry.get()
        processMessage(data, log, entry)
        
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data, log):
        mousePressed(event, data, log)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data, entry, log):
        keyPressed(event, data, entry, log)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data, log):
        timerFired(data, log)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, log)
        
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
    # set up events, specify per widget type
    canvas.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, log))
    canvas.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data, entry, log))
    entry.bind("<Key>", lambda event: entryKeyPressed(event, data, entry, log))
    timerFiredWrapper(canvas, data, log)
    
    # handles button click
    def buttonCallback():
        sendMsg(data, log, entry)
    
    # sets up button to send message
    button = Button(root, text = "Send", command = buttonCallback)
    button.grid(row = 2, column = 6)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    capture.release()
    cv2.destroyAllWindows()

run(800, 500)