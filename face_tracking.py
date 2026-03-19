import cv2
from djitellopy import Tello

class FaceTracker:
    def __init__(self):
        pass

    def findFace(self, img, cv2: cv2):
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        # Code to detect face using OpenCV or any other library
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 8)

        myFaceListC = []
        myFaceListArea = []

        for (x, y, w, h) in faces:
            cx = x + w // 2
            cy = y + h // 2
            area = w * h

            myFaceListC.append([cx, cy])
            myFaceListArea.append(area)

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if len(myFaceListArea) != 0:
            i = myFaceListArea.index(max(myFaceListArea))
            return img, [myFaceListC[i], myFaceListArea[i]]
        else:
            return img, [[0, 0], 0]
        
    """Not yet tested"""
    def trackFace(self, info, w, tello_controller: Tello): 
        x, y = info[0]
        area = info[1]

        fb = 0
        yaw = 0

        # LEFT / RIGHT
        if x < w//2 - 30:
            yaw = -30
        elif x > w//2 + 30:
            yaw = 30
        else:
            yaw = 0

        # FORWARD / BACKWARD
        if area > 8000:
            fb = -20
        elif area < 5000 and area != 0:
            fb = 20
        else:
            fb = 0

        # KHÔNG THẤY MẶT
        if x == 0:
            yaw = 0
            fb = 0

        tello_controller.send_rc_control(0, fb, 0, yaw)