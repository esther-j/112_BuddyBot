from widgets import subtitle
from tkinter import *

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
    subtitle(data, canvas, data.width / 4, data.height / 20, "What is BuddyChat?")
    helpText = """\
    BuddyChat is a chatting platform that lets you chat with a friend or our
    chatbot, BuddyBot! BuddyBot is a friendly, interactive chatbot who is always 
    down to have a conversation. BuddyChat comes with the feature of letting you 
    communicate the often unspoken - your feelings. Your chatting experience is
    also customizeable, allowing you to personalize it however you want. This
    includes turning off the emotion detection feature.
    """
    canvas.create_text(0, data.height / 5, text = helpText, font = "arial 20", anchor = NW)