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

class SettingsIcon(object):
    def __init__(self, len, height, leftCoordinate):
        self.color = "gray"
        self.len = len
        self.height = height
        self.coord = leftCoordinate
        
    def draw(self, canvas):
        for i in range(3):
            canvas.create_rectangle(self.coord, self.coord + 2 * i * self.height, self.coord + self.len, self.coord + self.height + 2 * i * self.height, fill = self.color, width = 0)
            
    def isPressed(self, mouseX, mouseY):
        if mouseX >= self.coord and mouseX <= self.coord + self.len:
            if mouseY >= self.coord and mouseY <= self.coord + (self.height * 5):
                return True
        return False
