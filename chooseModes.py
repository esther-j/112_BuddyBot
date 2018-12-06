### chooseModes

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