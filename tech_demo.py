"""Credits:
Live camera capture: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html#display-video
Face detection: https://docs.opencv.org/3.4.3/d7/d8b/tutorial_py_face_detection.html
"""

import cv2
import numpy as np

# Open camera and initialize the face cascade
capture = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("/Users/estherjang/Desktop/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

while(True):
    # Capture the frame from the video
    ret, frame = capture.read()
    
    # Find face and draw box in blue
    faces = faceCascade.detectMultiScale(frame, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y),(x + w, y + h), (255, 0, 0), 2)
    # Make window and show frames
    cv2.imshow("Face Detection", frame)
    # Do this every 10 ms
    cv2.waitKey(10)

# Stop camera capture and close windows
capture.release()
cv2.destroyAllWindows()