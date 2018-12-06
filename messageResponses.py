### messageResponses
### Contains all the different message handlers
### Has chatbot message responses
### Has user message processors

from tkinter import *
import random

# holds the current different message types
def messageType(data):
    greeting(data)
    question(data)
    farewell(data)

# chatbot responds to user entry using parsing method
def chatBotResponse(data, log):
    data.userEntry.lower().strip()
    typicalResponse = ["ok", "nice", "sounds interesting"]
    data.chatResponse = random.choice(typicalResponse)
    messageType(data)
    data.chatResponse = "BuddyBot: %s" % data.chatResponse
    data.chatLog.append(data.chatResponse)
    log.insert(END, "\n" + data.chatResponse)

# chatbot responds to user entry using chatterbot
def chatterBotResponse(data, log):
    reply = data.chatBot.get_response(data.userEntry)
    message = str(reply)
    newMsg = ""
    for c in message:
        if c != "-":
            newMsg += c
    data.chatResponse = newMsg.strip()
    data.chatResponse = "BuddyBot: %s" % data.chatResponse
    data.chatLog.append(data.chatResponse)
    log.insert(END, "\n" + data.chatResponse)

# Process the message sent by the bot by adding to log
def processBotMessage(data, log):
    log.config(state = NORMAL)
    log.insert(END, "\n" + data.chatResponse)
    data.chatLog.append(data.chatResponse)
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    
# chatbot processes the message said by user
def processMessage(data, log, entry):
    entry.delete(0, END)
    log.config(state = NORMAL)
    log.insert(END, "\nYou: %s" % data.userEntry)
    data.chatLog.append("You: %s" % data.userEntry)
    if data.useBot:
        # Have the chat response go by pre-defined algorithm 5% of the time and chatterbot elsewise
        chooseBotResponse = random.randint(0,19)
        if chooseBotResponse == 0:
            chatBotResponse(data, log)
        else:
            chatterBotResponse(data, log)
    log.yview_pickplace(END)
    log.config(state = DISABLED)
    
# chatbot processes the message said by user
def processFriendMessage(data, log, entry):
    entry.delete(0, END)
    log.config(state = NORMAL)
    log.insert(END, "\nFriend: %s" % data.userEntry)
    data.chatLog.append("Friend: %s" % data.userEntry)
    if data.useBot:
        # Have the chat response go by pre-defined algorithm 5% of the time and chatterbot elsewise
        chooseBotResponse = random.randint(0,19)
        if chooseBotResponse == 0:
            chatBotResponse(data, log)
        else:
            chatterBotResponse(data, log)
    log.yview_pickplace(END)
    log.config(state = DISABLED)     
        
# respond to different emotions
def respondToEmotion(emotion, data, log):
    msg = ""
    if emotion == "happy":
        happyResponses = ["I'm glad you're happy! That makes me happy too :)",
                        "Did something exciting happen? You seem happy!",
                        "Seeing you smile makes me smile too :)",
                        "You seem happy recently, by the way. Yay!"]
        msg = random.choice(happyResponses)
    elif emotion == "sad":
        sadResponses = ["You seem sad recently. What's up?",
                        "What's making you feel down, by the way?",
                        "I noticed that you seem sad. Want to talk about it?"]
        msg = random.choice(sadResponses)
    elif emotion == "angry":
        angryResponses = ["Ah! You seem kind of angry recently",
                        "You seem upset. What's wrong?"]
        msg = random.choice(angryResponses)
    elif emotion == "surprised":
        surpriseResponses = ["Did something happen? Why do you seem surprised?"
                            "What's new? You look surprised"]
        msg = random.choice(surpriseResponses)
    if len(msg) != 0:
        data.chatResponse = "BuddyBot: %s" % msg
        processBotMessage(data, log)