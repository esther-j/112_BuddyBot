""" Credit for UI:
"Updated Animation Starter Code" template from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
Entry Box Tutorial: http://effbot.org/tkinterbook/entry.htm
Understanding .pack(): http://effbot.org/tkinterbook/pack.htm
Text Tutorials: https://www.tutorialspoint.com/python/tk_text.htm http://effbot.org/tkinterbook/text.htm
ScrollBat Tutorial: http://effbot.org/zone/tkinter-scrollbar-patterns.htm
Grid Tutorial: http://effbot.org/tkinterbook/grid.htm
Button Tutorial: http://effbot.org/tkinterbook/button.htm
Events and Binding Tutorial: http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
Mode idea: https://www.cs.cmu.edu/~112/notes/notes-animations-demos.html#modeDemo
Tkinter Colors: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

Credit for ChatterBot tutorial: ChatterBot tutorial from https://www.youtube.com/watch?v=3k8OFy-etoo

Credit for Sockets Tutorial (dots_client.py): https://drive.google.com/drive/folders/0B3Jab-H-9UIiZ2pXMExjdDV1dW8
"""

from helpMode import *
from startMode import *
from settingsMode import *
from widgets import *
from emotionReader import *
from tkinter import *
import time
from drawChatbot import *
from chatbotAnswer import *
from tkinter import *
import random
import cv2
import numpy as np
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import socket
import threading
from queue import Queue

HOST = "128.237.186.41" # put your IP address here if playing on multiple computers
PORT = 50010

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

def init(data): 
    data.timer = 0
    data.blink = False
    data.mode = "start" 
    data.botColor = "LightBlue1"
   # setupChatBot(data)
    makeButtons(data)
    makeSettingsIcon(data)
    makeSettingsOptions(data)
    data.chatLog = []
    data.overallEmotions = []
    data.userEntry = ""
    data.previousMode = ""
    data.useBot = True
    data.colorOptions = ["LightBlue1", "red", "orange", "yellow", "green", "blue", "purple"]
    data.chatResponse = ""
    data.emotion = "happy"
    #trainEmotionDetector()
    data.detectFace = False

def setupChatBot(data):
    data.chatBot = ChatBot("buddyBot")
    data.chatBot.set_trainer(ListTrainer)
    
    trainingData  = "/Users/estherjang/Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/"
    
    for files in os.listdir(trainingData):
            trainingFile = open(trainingData + files, 'r').readlines()
            data.chatBot.train(trainingFile)

def makeSettingsOptions(data):
    data.goHomeOption = SettingsOption(data.width / 6, data.height / 5, data.width / 30, "Go back home", "dark grey", data.height // 18)
    data.changeColorOption = SettingsOption(data.width / 6, data.height * 3 / 10, data.width / 30, "Change bot color", data.botColor, data.height // 18)
    data.faceDetectionOption = SettingsOption(data.width / 6, data.height * 2 / 5, data.width / 30, "Turn off face detection (currently on)", "dark grey", data.height // 18)
    data.clearLogOption = SettingsOption(data.width / 6, data.height / 2, data.width / 30, "Clear log", "dark grey", data.height // 18)

def makeSettingsIcon(data):
    lineLen = data.width / 25
    lineHeight = data.height / 90
    leftCor = data.width / 40
    data.settingsIcon = SettingsIcon(lineLen, lineHeight, leftCor)    

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
    
    data.botModeButton = ScreenButton(data, data.width / 4, data.height / 2, "BuddyBot Chat")
    data.friendModeButton = ScreenButton(data, data.width * 3 / 4, data.height / 2, "Friend Chat")
    data.botModeButton.width = data.width / 6
    data.botModeButton.height = data.height / 4
    data.friendModeButton.width = data.width / 6
    data.friendModeButton.height = data.height / 4
    
def mousePressed(event, data, log): 
    if data.mode == "start": 
        startMousePressed(event, data)
    elif data.mode == "settings":
        settingsMousePressed(event, data, log)
    elif data.mode == "run":
        runMousePressed(event, data)
    elif data.mode == "help":
        helpMousePressed(event, data)
    elif data.mode == "friend":
        friendMousePressed(event, data)
    elif data.mode == "modes":
        modesMousePressed(event, data)

def keyPressed(event, data): 
    if data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "settings":
        settingsKeyPressed(event, data)
    elif data.mode == "run":
        runKeyPressed(event, data)
    elif data.mode == "help":
        helpKeyPressed(event, data)
    elif data.mode == "friend":
        friendKeyPressed(event, data)
    elif data.mode == "modes":
        modesKeyPressed(event, data)
        
def timerFired(data, log, entry): 
    if data.mode == "start":
        startTimerFired(data)
    elif data.mode == "settings":
        settingsTimerFired(data)
    elif data.mode == "run":
        runTimerFired(data, log, entry)
    elif data.mode == "help":
        helpTimerFired(data)
    elif data.mode == "friend":
        friendTimerFired(data, log, entry)
    elif data.mode == "modes":
        modesTimerFired(data)
        
def redrawAll(canvas, data, entry, scrollBar, log, button): 
    if data.mode == "start":
        eraseWidgets(log, entry, button, scrollBar, canvas)
        startRedrawAll(canvas, data)
    elif data.mode == "settings":
        eraseWidgets(log, entry, button, scrollBar, canvas)
        settingsRedrawAll(canvas, data)
    elif data.mode == "run":
        if data.previousMode != "run":
            print("cleared in log")
            clearLog(log)
            del data.chatLog[:]
        data.useBot = True
        drawWidgets(log, entry, button, scrollBar, canvas)
        runRedrawAll(canvas, data)
        data.previousMode = "run"
    elif data.mode == "help":
        helpRedrawAll(canvas, data)
    elif data.mode == "friend":
        if data.previousMode != "friend":
            print("cleared in friend")
            clearLog(log)
            del data.chatLog[:]
        data.useBot = False
        drawWidgets(log, entry, button, scrollBar, canvas)
        friendRedrawAll(canvas, data)
        data.previousMode = "friend"
    elif data.mode == "modes":
        eraseWidgets(log, entry, button, scrollBar, canvas)
        modesRedrawAll(canvas, data)

def drawWidgets(log, entry, button, scrollBar, canvas):
    entry.grid(row = 2, columnspan = 6)
    canvas.grid(row = 0, columnspan = 8)
    scrollBar.grid(row = 1, column = 7)
    log.grid(row = 1, columnspan = 7)
    button.grid(row = 2, column = 6)
    
def eraseWidgets(log, entry, button, scrollBar, canvas):
    log.grid_forget()
    entry.grid_forget()
    button.grid_forget()
    scrollBar.grid_forget()
    button.grid_forget()
    
def modesMousePressed(event, data):
    if data.botModeButton.isPressed(event.x, event.y):
        data.mode = "run"
    elif data.friendModeButton.isPressed(event.x, event.y):
        data.mode = "friend"
    elif data.backButton.isPressed(event.x, event.y):
        data.mode = "start"

def modesKeyPressed(event, data):
    pass

def modesTimerFired(data):
    pass
    
def modesRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "LightBlue1", width = 0)
    data.botModeButton.draw(canvas)
    data.friendModeButton.draw(canvas)
    data.backButton.draw(canvas)
    
def friendMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "settings"

def friendKeyPressed(event, data):
    pass

def friendTimerFired(data, log, entry):
    runTimerFired(data, log, entry)
    
def friendRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = data.botColor, width = 0)
    pixelLen = data.width / 30
    drawEyes(canvas, data, pixelLen)   
    if data.emotion == "sad":
        drawSadMouth(canvas, data, pixelLen)
    elif data.emotion == "surprised":
        drawSurprisedMouth(canvas, data, pixelLen)
    else:
        drawHappyMouth(canvas, data, pixelLen)
    data.settingsIcon.color = "dark gray"
    data.settingsIcon.draw(canvas)
    
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
    data.chatResponse = "BuddyBot: %s" % data.chatResponse
    data.chatLog.append(data.chatResponse)
    log.insert(END, "\n" + data.chatResponse)

def chatterBotResponse(data, log):
    reply = data.chatBot.get_response(data.userEntry)
    message = str(reply)
    newMsg = ""
    for c in message:
        if c != "-":
            newMsg += c
    data.chatResponse = newMsg.strip()
    data.chatResponse = "BuddyBot: %s" % data.chatResponse
    data.chatLog.append(data.chatResponse)
    log.insert(END, "\n" + data.chatResponse)

def processBotMessage(data, log, entry):
    entry.delete(0, END)
    log.config(state = NORMAL)
    print("ERROR HERE?")
    log.insert(END, "\n" + data.chatResponse)
    data.chatLog.append(data.chatResponse)
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    print(data.chatLog)
    
# chatbot processes the message said by user
def processMessage(data, log, entry):
    entry.delete(0, END)
    log.config(state = NORMAL)
    log.insert(END, "\nYou: %s" % data.userEntry)
    data.chatLog.append("You: %s" % data.userEntry)
    if data.useBot:
        chatBotResponse(data, log)
    # chatterBotResponse(data, log)
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    print(data.chatLog)
    
# chatbot processes the message said by user
def processFriendMessage(data, log, entry):
    entry.delete(0, END)
    log.config(state = NORMAL)
    log.insert(END, "\nFriend: %s" % data.userEntry)
    data.chatLog.append("Friend: %s" % data.userEntry)
    if data.useBot:
        chatterBotResponse(data, log)
    # chatBotResponse(data, log)
    log.yview_pickplace(END)
    log.config(state = DISABLED) 
    print(data.chatLog)
    
# when return key is pressed, submit message
def entryKeyPressed(event, data, entry, log):
    msg = ""
    
    entryLog = entry.get()
    if event.keysym == "Return" and len(entryLog) > 0:
        data.userEntry = entryLog
        processMessage(data, log, entry)
        numWords = 0
        for i in data.userEntry.split():
            numWords += 1
        if data.useBot:
            msg = "sent: bot %s %d %s" % (data.mode, numWords, data.userEntry)
            msg += " %s" % (data.chatResponse)
        else:
            msg = "sent: no %s %d %s" % (data.mode, numWords, data.userEntry)
        msg += "\n"
        
    if (msg != ""):
      print("sending: ", msg)
      data.server.send(msg.encode())
        
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
    msg = ""
    
    entryLog = entry.get()
    data.userEntry = entry.get()
    processMessage(data, log, entry)
    numWords = 0
    for i in data.userEntry.split():
        numWords += 1
    if data.useBot:
        msg = "sent: bot %s %d %s" % (data.mode, numWords, data.userEntry)
        msg += " %s" % (data.chatResponse)
    else:
        msg = "sent: no %s %d %s" % (data.mode, numWords, data.userEntry)
    msg += "\n"
        
    if (msg != ""):
        print("sending: ", msg)
        data.server.send(msg.encode())
        
def runMousePressed(event, data):
    if data.settingsIcon.isPressed(event.x, event.y):
        data.mode = "settings"
    
def runKeyPressed(event, data):
    pass
    
def runTimerFired(data, log, entry):
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]
            if command == "sent:":
                if msg[3] == data.mode:
                    userMsg = ""
                    if msg[2] == "bot":
                        lenEntry = int(msg[4])
                        for i in range(5, 5 + lenEntry):
                            userMsg += msg[i] + " "
                        startBotEntry = 5 + lenEntry
                        botMsg = ""
                        for i in range(startBotEntry, len(msg)):
                            botMsg += msg[i] + " "
                        data.userEntry = userMsg
                        data.useBot = False
                        processFriendMessage(data, log, entry)
                        data.useBot = True
                        data.chatResponse = botMsg
                        processBotMessage(data, log, entry)
                    else:
                        for i in range(5, len(msg)):
                            userMsg += msg[i] + " "
                        data.userEntry = userMsg
                        processFriendMessage(data, log, entry)
                
        except:
            print("failed")
        serverMsg.task_done()
                
            
    data.timer += 1
    cap = cv2.VideoCapture(0)
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
            data.emotion = mainEmotion
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
    if data.emotion == "sad":
        drawSadMouth(canvas, data, pixelLen)
    elif data.emotion == "surprised":
        drawSurprisedMouth(canvas, data, pixelLen)
    else:
        drawHappyMouth(canvas, data, pixelLen)
    data.settingsIcon.color = "dark gray"
    data.settingsIcon.draw(canvas)


    #################################### # use the run function as-is #################################### 
def run(width=300, height=300, serverMsg = None, server = None):
    def redrawAllWrapper(canvas, data, entry, scrollBar, log, button):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data, entry, scrollBar, log, button)
        canvas.update()

    def mousePressedWrapper(event, canvas, data, entry, scrollBar, log, button):
        mousePressed(event, data, log)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)

    def keyPressedWrapper(event, canvas, data, entry, scrollBar, log, button):
        keyPressed(event, data, entry, log)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)

    def timerFiredWrapper(canvas, data, entry, scrollBar, log, button):
        timerFired(data, log, entry)
        redrawAllWrapper(canvas, data, entry, scrollBar, log, button)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data, entry, scrollBar, log, button)
        
    capture = cv2.VideoCapture(0)
    faceCascade = cv2.CascadeClassifier("/Users/estherjang/Desktop/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
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

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(800, 500, serverMsg, server)
cv2.destroyAllWindows()
cap.release()