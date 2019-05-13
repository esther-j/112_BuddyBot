# BuddyChat
BuddyChat is a chatting platform that allows you to chat with a friend, with a chatbot, BuddyBot, or both at the same time! BuddyBot can read emotions, express them, and talk them out with users, allowing a more interactive chatting experience. There are also many extra features for users including clearing and saving chat logs, changing the view of the chat, and disabling emotion recognition. 

### Necessary Modules
Please install the following python modules (by typing "pip install <module>" into the shell):
 * cv2
 * chatterbot
 * chatterbot.trainers
 * numpy
 * socket
 * threading
 * queue

### Dataset for emotion detection (Note: only required if running emotion detection)
You will need a dataset of images with different examples of each emotion in order to run the emotion detection. In order to make this dataset, create a folder called "dataset" with subfolders of emotions: "happy," "sad," "neutral," "angry," and "surprised." Put images of sizes (350x350) that have a person displaying the given emotion. Preferably, the image will be the person's entire face and not have too much background. Make sure that emotionReader.py can reach this directory.

### Running
1. In order to run this program, first open up chatbotServer.py. Here, change HOST to your own IP address. Then, run chatbotServer in your terminal/shell.
  
2. Next, open up main.py and a new terminal/shell. With all the necessary modules installed, run this program. You will likely have to wait 1-2 minutes for chatterbot and your emotion dataset to train. 

3. The BuddyChat platform should be up and running now! You may add a maximum of one more concurrent user by repeating the previous step. 

### Youtube video:
https://www.youtube.com/watch?v=eCi3k_m1si8
