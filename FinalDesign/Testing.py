import cv2
import sys
import time
import serial
import RPi.GPIO as gpio
from picamera import PiCamera
import unicornhat as uhat

import UnicornControl as uctrl
import GPIOControl as gctrl

#####SETUP AND CONFIGURATION#####

#Aruco Setup
arucoDict = cv2.aruco.Dictionary_create(4,4)
arucoParams = cv2.aruco.DetectorParameters_create()

#Camera Setup
cam = cv2.VideoCapture(0)
if(cam.isOpened == False):
    sys.exit()
_, img = cam.read()
cam.release()
print(img.shape)
imgCenterX = img.shape[1]/2

#################################

class gate:
    def __init__(self, corners, ID):
        self.ID = ID
        self.corners = corners
        self.size = abs(corners[0][0] - corners[1][0])

    
def noGates():
    uhat.set_pixel(0,0,255,0,0)
    uhat.show()
    
def GateRecognized():
    uhat.set_pixel(0,0,0,255,0)
    uhat.show()

while(True):
    cam = cv2.VideoCapture(0)
    if(cam.isOpened == False):
        sys.exit()
    tags = []
    _, img = cam.read()
    cam.release()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)
    
    if(cornerpts == [] or len(ids) == 1):
        noGates()

    else:
        print(len(ids), '\n')
        print(ids)
        for j in range(len(ids)):
            g = gate(cornerpts[j][0], ids[j])
            tags.append(g)           

        tags.sort(key = lambda gate: gate.size, reverse = True)
        
        if((tags[0].ID == 0 and tags[1].ID == 1) or  (tags[0].ID == 1 and tags[1].ID == 0)):
            target = (tags[0].corners[0][0] + tags[1].corners[1][0]) / 2
            GateRecognized()
        else:
            noGates()

cam.release()