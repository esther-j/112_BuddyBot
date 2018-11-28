"""
Credit: Adapted code from http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/

Official citation:
van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset. A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/
"""
import cv2
import random
import numpy as np
import os
import time

classifier = cv2.CascadeClassifier("/Users/estherjang/Documents/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

foundEmotions = []
# set up the emotions
emotions = ["happy", "neutral", "sad", "angry", "surprised"]
# create emotion detector object
emotionDetector = cv2.face.FisherFaceRecognizer_create() 
# train the emotion detector
trainEmotionDetector()
# turn on camera
cap = cv2.VideoCapture(0)

# gets all the images from the dataset of a given emotion
def getImages(emotion):
    allImages = []
    path = "/Users/estherjang/Desktop/dataset/%s" % emotion
    if os.path.isdir(path):
        for image in os.listdir(path):
            if image != (".DS_Store"):
                allImages.append("%s/%s" % (path, image))
    return allImages

# loads all the images for each emotion and trains face recognizer
def trainEmotionDetector():
    trainingImages = []
    labels = []
    # for each emotion, get the necessary images, convert to grey, add to data
    for emotion in emotions:
        images = getImages(emotion)
        for face in images:
            image = cv2.imread(face)
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # add the image and its given label to the data
            trainingImages.append(grayImage)
            labels.append(emotions.index(emotion))
    print("Currently have %d images" % len(trainingImages))
    print("Started training...", end = "")
    emotionDetector.train(trainingImages, np.asarray(labels))
    print("Done training")

# returns whether a face is seen or not
# looks for a face and writes the face as a temp file if finds one 
def findFace(frame):
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = classifier.detectMultiScale(grayImg, 1.3, 5)
    
    # if face(s) detected, then pull out face and resize it
    # as a 350 x 350 image and write it as a temporary image file
    if len(face) != 0:
        (x, y, w, h) = face[0]
        grayFace = grayImg[y:(y + h), x:(x + w)]
        resized = cv2.resize(grayFace, (350, 350))
        cv2.imwrite("tmpImg.jpg", resized)
        return True, (x, y, w, h)
    return False, None

# draws box around face and writes emotion
def displayInformation(img, rectangle, emotion):
    yellow = (0, 255, 255)
    (x, y, w, h) = rectangle
    cv2.rectangle(img, (x, y), (x + w, y + h), yellow, 2)
    cv2.putText(img, emotion, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.5, yellow, 2)

# finds the most commonly appeared emotion and returns that
def predictOverallEmotion(lst):
    mostCommonEmotion = ""
    freqEmotion = 0
    for emotion in emotions:
        if lst.count(emotion) > freqEmotion:
            mostCommonEmotion = emotion
            freqEmotion = lst.count(emotion)
    return mostCommonEmotion

def getEmotion():
    ret, frame = cap.read()
    # looks for face + creates image of it if face is found
    foundFaceInfo = findFace(frame)
    foundFace = foundFaceInfo[0]
    faceCoords = foundFaceInfo[1]
    
    if foundFace:
        image = cv2.imread("tmpImg.jpg")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # predict what emotion the current frame is holding
        pred, conf = emotionDetector.predict(gray)
        emotion = emotions[pred]
        foundEmotions.append(emotion)
        displayInformation(frame, faceCoords, emotion)
        cv2.imshow("Emotion Detector", frame)
        # delete temporary image
        os.remove("tmpImg.jpg")
        return emotion
    # if face is not found, then return information indicating that
    else:
        cv2.putText(frame, "Don't see face", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
        cv2.imshow("Emotion Detector", frame)
        return None