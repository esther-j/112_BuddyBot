from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

bot = ChatBot("Bot")
bot.set_trainer(ListTrainer)

trainingData  = "/Users/estherjang/Downloads/chatterbot-corpus-master/chatterbot_corpus/data/english/"

for files in os.listdir(trainingData):
        data = open(trainingData + files, 'r').readlines()
        bot.train(data)
        
while True:
    message = input("You:")
    if message.strip() != "Bye":
        reply = bot.get_response(message)
        message = str(reply)
        newMsg = ""
        for s in message:
            if s != "-":
                newMsg += s
        message = newMsg.strip()
        print(message)


