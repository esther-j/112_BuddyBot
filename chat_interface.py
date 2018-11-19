""" Credit:
"Updated Animation Starter Code" template from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
Entry Box Tutorial: http://effbot.org/tkinterbook/entry.htm
Understanding .pack(): http://effbot.org/tkinterbook/pack.htm
Text Tutorials: https://www.tutorialspoint.com/python/tk_text.htm http://effbot.org/tkinterbook/text.htm
"""

from tkinter import *
import random

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.chatLog = []
    data.userEntry = ""
    data.botResponded = True
    data.chatResponse = ""
    pass

def mousePressed(event, data):
    # use event.x and event.y
    pass

def chatBotResponse(data, log):
    data.responded = False
    data.userEntry.lower().strip()
    data.chatResponse = "ok"
    greeting(data)
    question(data)
    log.insert(END, "\n" + data.chatResponse)
    data.responded = True

def question(data):
    answers = ["I don't know", "no", "yes"]
    if data.userEntry[-1] == "?":
        data.chatResponse = random.choice(answers)

def greeting(data):
    greetings = ["hello", "hi", "hallo", "hai", "hey"]
    if data.userEntry in greetings:
        data.chatResponse = random.choice(greetings)

def keyPressed(event, data, entry, log):
    entryLog = entry.get()
    if event.keysym == "Return" and len(entryLog) > 0 and data.botResponded:
        data.userEntry = entryLog
        entry.delete(0, END)
        data.chatLog.append(data.userEntry)
        log.config(state = NORMAL)
        log.insert(END, "\n" + data.userEntry)
        chatBotResponse(data, log)
        log.yview_pickplace(END)
        log.config(state = DISABLED)
        print(data.chatLog)
    # use event.char and event.keysym

def timerFired(data):
    # userInput = entry.get()
    # print(userInput)
    pass

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "sky blue", width = 0)
    pixelLen = data.width / 30
    drawEyes(canvas, data, pixelLen)
    drawMouth(canvas, data, pixelLen)
    
def drawEyes(canvas, data, pixelLen):
    halfPixel = pixelLen / 2
    canvas.create_rectangle(data.width / 4 - halfPixel, data.height / 3 - halfPixel, data.width / 4 + halfPixel, data.height / 3 + halfPixel, fill = "black")
    canvas.create_rectangle(data.width * (3 / 4) - halfPixel, data.height / 3 - halfPixel, data.width * (3 / 4) + halfPixel, data.height / 3 + halfPixel, fill = "black")
    
def drawMouth(canvas, data, pixelLen):
    canvas.create_rectangle(data.width / 3, data.height / 3 + (pixelLen * 3), data.width * 2 / 3, data.height / 3 + (pixelLen * 4), fill = "black")
    canvas.create_rectangle(data.width / 3 - pixelLen, data.height / 3 + (pixelLen * 2), data.width / 3, data.height / 3 + (pixelLen * 3), fill = "black")
    canvas.create_rectangle(data.width * 2 / 3, data.height / 3 + (pixelLen * 2), data.width * 2 / 3 + pixelLen, data.height / 3 + (pixelLen * 3), fill = "black")
    
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

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data, entry, log):
        keyPressed(event, data, entry, log)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    
    entry = Entry(root)
    entryWidth = data.width // 10
    entry.config(width = entryWidth)
    entry.pack(side = BOTTOM)
    
    scrollBar = Scrollbar(root)
    
    logWidth = data.width // 8
    logHeight = data.height // 100
    log = Text(root, width = logWidth, height = logHeight, yscrollcommand = scrollBar.set, state = DISABLED)
    scrollBar.config(command=log.yview)
    
    log.pack(side = BOTTOM)
   # log.pack(side = LEFT)
    scrollBar.pack(side = RIGHT, fill = Y)
    
    root.resizable(width=True, height=True) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data, entry, log))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 500)