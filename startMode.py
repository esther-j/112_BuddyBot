import cv2

###### start mode 
def startMousePressed(event, data):
    if data.startButton.isPressed(event.x, event.y):
        data.mode = "modes"
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