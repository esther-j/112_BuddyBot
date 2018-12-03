import random 

# user message is a question
def question(data):
    answers = ["I don't know", "no", "yes"]
    if len(data.userEntry) > 0 and data.userEntry[-1] == "?":
        data.chatResponse = random.choice(answers)
        yesNoQuestion(data)
        specificQuestion(data)
    elif len(data.userEntry) >= 3:
        startKey = ["why", "how", "who", "what", "wat", "when", "where"]
        if data.userEntry.split()[0] in startKey:
            specificQuestion(data)

# user message is a yes/no question
def yesNoQuestion(data):
    firstWord = data.userEntry.split()[0]
    startKey = ["should", "could", "is", "are"]
    responses = ["yes", "no", "I don't know", ]
    if firstWord in startKey:
        data.chatResponse = random.choice(responses)

# user message is a question requiring a specific answer
def specificQuestion(data):
    words = [""] * 4
    for i in range(len(data.userEntry.split())):
        if i < 4: 
            words[i] = data.userEntry.split()[i]
    for i in range(len(words)):
        if len(words[i]) > 0:
            if words[i][-1] == "?":
                words[i] = words[i][:-1]
    startKey = ["why", "how", "who", "what", "wat", "when", "where"]
    responses = ["what do you think?", "good question", "not sure"]
    definingWord = ["the", "a", "your", "my"]
    adjectives = ["funny", "happy", "weird", "cool", "fuzzy", "orange", "sad"]
    
    # parse through question words, looking for keywords
    if words[0] in startKey:
        # see if an object is being asked about
        if words[1] in ["is", "are"]:
            # see if bot is being talked about
            if words[2] == "you":
                data.chatResponse = "I am " + random.choice(adjectives)
            elif words[2] == "your" and words[3] != "":
                data.chatResponse = "My %s is %s" % (words[3], random.choice(adjectives))
            elif words[2] == "my" and words[3] != "":
                data.chatResponse = "Your %s is %s" % (words[3], random.choice(adjectives))
            elif words[2] in definingWord:
                data.chatResponse = "%s %s %s %s" % (words[2], words[3], words[1], random.choice(adjectives))
            else:
                data.chatResponse = "%s %s %s" % (words[2], words[1], random.choice(adjectives))
        else:
            data.chatResponse = random.choice(responses)

# user said a greeting
def greeting(data):
    greetings = ["hello", "hi", "hallo", "hai", "hey", "sup"]
    if data.userEntry in greetings:
        data.chatResponse = random.choice(greetings)

# user said a farewell
def farewell(data):
    farewells = ["bye", "good bye", "see ya"]
    if data.userEntry in farewells:
        data.chatResponse = random.choice(farewells)