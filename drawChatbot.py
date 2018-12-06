### Draw the bot!
from tkinter import *

# pixeled wip: going to add pixel mode of drawing

# # draws the bot's eyes
# def drawEyes(canvas, data, pixelLen):
#     halfPixel = pixelLen / 2
#     canvas.create_rectangle(data.width / 4 - halfPixel, data.height / 3 - halfPixel, data.width / 4 + halfPixel, data.height / 3 + halfPixel, fill = "black")
#     canvas.create_rectangle(data.width * (3 / 4) - halfPixel, data.height / 3 - halfPixel, data.width * (3 / 4) + halfPixel, data.height / 3 + halfPixel, fill = "black")
# 
# # draws the bot's mouth
# def drawMouth(canvas, data, pixelLen):
#     canvas.create_rectangle(data.width / 3, data.height / 3 + (pixelLen * 3), data.width * 2 / 3, data.height / 3 + (pixelLen * 4), fill = "black")
#     canvas.create_rectangle(data.width / 3 - pixelLen, data.height / 3 + (pixelLen * 2), data.width / 3, data.height / 3 + (pixelLen * 3), fill = "black")
#     canvas.create_rectangle(data.width * 2 / 3, data.height / 3 + (pixelLen * 2), data.width * 2 / 3 + pixelLen, data.height / 3 + (pixelLen * 3), fill = "black")

# draws the bot's eyes
def drawEyes(canvas, data, pixelLen):
    halfPixel = pixelLen / 2
    canvas.create_oval(data.width / 4 - halfPixel, data.height / 3 - halfPixel, data.width / 4 + halfPixel, data.height / 3 + halfPixel, fill = "black")
    canvas.create_oval(data.width * (3 / 4) - halfPixel, data.height / 3 - halfPixel, data.width * (3 / 4) + halfPixel, data.height / 3 + halfPixel, fill = "black")
    
# draws the bot's happy mouth
def drawHappyMouth(canvas, data, pixelLen):
    canvas.create_arc(data.width * 2 / 5, data.height / 2, data.width * 3 / 5, data.height / 3, start = 0, extent = -180, style = ARC, width = 10)

# draws bot's sad mouth
def drawSadMouth(canvas, data, pixelLen):
    canvas.create_arc(data.width * 2 / 5, data.height * 5 / 12, data.width * 3 / 5, data.height * 7 / 12, start = 0, extent = 180, style = ARC, width = 10)
    
# draws bot's surprised mouth
def drawSurprisedMouth(canvas, data, pixelLen):
    canvas.create_oval(data.width * 9 / 20, data.height / 3, data.width * 11 / 20, data.height / 2, fill = "black")