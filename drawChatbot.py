# Draw the bot!

# draws the bot's eyes
def drawEyes(canvas, data, pixelLen):
    halfPixel = pixelLen / 2
    canvas.create_rectangle(data.width / 4 - halfPixel, data.height / 3 - halfPixel, data.width / 4 + halfPixel, data.height / 3 + halfPixel, fill = "black")
    canvas.create_rectangle(data.width * (3 / 4) - halfPixel, data.height / 3 - halfPixel, data.width * (3 / 4) + halfPixel, data.height / 3 + halfPixel, fill = "black")

# draws the bot's mouth
def drawMouth(canvas, data, pixelLen):
    canvas.create_rectangle(data.width / 3, data.height / 3 + (pixelLen * 3), data.width * 2 / 3, data.height / 3 + (pixelLen * 4), fill = "black")
    canvas.create_rectangle(data.width / 3 - pixelLen, data.height / 3 + (pixelLen * 2), data.width / 3, data.height / 3 + (pixelLen * 3), fill = "black")
    canvas.create_rectangle(data.width * 2 / 3, data.height / 3 + (pixelLen * 2), data.width * 2 / 3 + pixelLen, data.height / 3 + (pixelLen * 3), fill = "black")

# draws settings
def drawSettings(canvas, data):
    lineLen = data.width / 25
    lineHeight = data.width / 120
    leftCor = data.width / 40
    for i in range(3):
        canvas.create_rectangle(leftCor, leftCor + 2 * i * lineHeight, leftCor + lineLen, leftCor + lineHeight + 2 * i * lineHeight, fill = "dark grey", width = 0)