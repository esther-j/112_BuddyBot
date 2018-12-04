# from chatterbot import ChatBot
# chatbot = ChatBot(
#     "BuddyBot",
#     storage_adapter = "chatterbot.storage.SQLStorageAdapter",
#     database = "./database.sqlite",
#     input_adapter = "chatterbot.input.TerminalAdapter"
#     output_adapter = "chtterbot.output.TerminalAdapter".
#     logic_adapters = [
#                     "chatterbot.logic.MathematicalEvaluation",
#                     "chatterbot.logic.TimeLogicAdapter"
#                     ]
#     )
#     
# while True:
#     try:
#         bot_input = bot.get_response(None)
#     
#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break


# from chatterbot import ChatBot
# 
# # Uncomment the following lines to enable verbose logging
# # import logging
# # logging.basicConfig(level=logging.INFO)
# 
# # Create a new instance of a ChatBot
# bot = ChatBot(
#     "SQLMemoryTerminal",
#     storage_adapter='chatterbot.storage.SQLStorageAdapter',
#     logic_adapters=[
#         "chatterbot.logic.MathematicalEvaluation",
#         "chatterbot.logic.TimeLogicAdapter",
#         "chatterbot.logic.BestMatch"
#     ],
#     input_adapter="chatterbot.input.TerminalAdapter",
#     output_adapter="chatterbot.output.TerminalAdapter",
# )
# 
# print("Type something to begin...")
# 
# # The following loop will execute each time the user enters input
# while True:
#     try:
#         # We pass None to this method because the parameter
#         # is not used by the TerminalAdapter
#         bot_input = bot.get_response(None)
# 
#     # Press ctrl-c or ctrl-d on the keyboard to exit
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from settings import Microsoft

'''
See the Microsoft DirectLine api documentation for how to get a user access token.
https://docs.botframework.com/en-us/restapi/directline/
'''

chatbot = ChatBot(
    'MicrosoftBot',
    directline_host=Microsoft['directline_host'],
    direct_line_token_or_secret=Microsoft['direct_line_token_or_secret'],
    conversation_id=Microsoft['conversation_id'],
    input_adapter='chatterbot.input.Microsoft',
    output_adapter='chatterbot.output.Microsoft'
)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')

# The following loop will execute each time the user enters input
while True:
    try:
        response = chatbot.get_response('')

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
