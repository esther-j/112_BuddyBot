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
    chatbot, BuddyBot! You can 
    
    BuddyBot is a friendly, interactive chatbot who is always down to have a 
    conversation. BuddyBot can also detect emotions and wants to talk them out 
    with you. The bot is also customizable so you can personalize it however you
    want. This includes turning off face detection. 
    """
    canvas.create_text(0, data.height / 5, text = helpText, font = "arial 20", anchor = NW)