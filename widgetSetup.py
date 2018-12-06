### Widget setup
### Initializes the personalized widget objects

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os 
from widgets import *

# set up and train the chatterbot
def setupChatBot(data):
    data.chatBot = ChatBot("BuddyBot")
    data.chatBot.set_trainer(ListTrainer)
    
    trainingData  = "/Users/estherjang/Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/"
    
    for files in os.listdir(trainingData):
            trainingFile = open(trainingData + files, 'r').readlines()
            data.chatBot.train(trainingFile)

# Initialize the settings options
def makeSettingsOptions(data):
    data.goHomeOption = SettingsOption(data.width / 6, data.height / 5, data.width / 30, "Go back home", "dark grey", data.height // 18)
    data.changeColorOption = SettingsOption(data.width / 6, data.height * 3 / 10, data.width / 30, "Change bot color", data.botColor, data.height // 18)
    data.faceDetectionOption = SettingsOption(data.width / 6, data.height * 2 / 5, data.width / 30, "Turn off face detection (currently on)", "dark grey", data.height // 18)
    data.clearLogOption = SettingsOption(data.width / 6, data.height / 2, data.width / 30, "Clear log", "dark grey", data.height // 18)
    data.saveLogOption = SettingsOption(data.width / 6, data.height * 3 / 5, data.width / 30, "Save log", "dark grey", data.height // 18)

# Initializes the settings icon
def makeSettingsIcon(data):
    lineLen = data.width / 25
    lineHeight = data.height / 90
    leftCor = data.width / 40
    data.settingsIcon = SettingsIcon(lineLen, lineHeight, leftCor)    

# Initializes the buttons on the screen
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