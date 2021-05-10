import cv2
import sys
import time
import serial
import RPi.GPIO as gpio
from picamera import PiCamera

import GPIOControl as gctrl

#####SETUP AND CONFIGURATION#####

#Tag IDS
LEFT = 0
RIGHT = 1
START = 2
STOP = 3

#Pin Definitions
HR = 26
R = 19
S = 13
L = 6
HL = 5

START_DETECTED = 21
NO_GATE = 16
NEW_GATE = 20

#Serial Port
uart = serial.Serial(
    port='/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

#Pin Setup
gpio.setmode(gpio.BCM)
gpio.setup(HL, gpio.OUT)
gpio.setup(L, gpio.OUT)
gpio.setup(S, gpio.OUT)
gpio.setup(R, gpio.OUT)
gpio.setup(HR, gpio.OUT)
gpio.setup(NEW_GATE, gpio.OUT)
gpio.setup(NO_GATE, gpio.OUT)
gpio.setup(START_DETECTED, gpio.OUT)

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
        self.size = abs(corners[3][1] - corners[0][1])

def resetPins():
    gpio.output(HR, gpio.LOW)
    gpio.output(R, gpio.LOW)
    gpio.output(S, gpio.LOW)
    gpio.output(L, gpio.LOW)
    gpio.output(HL, gpio.LOW)
    gpio.output(NO_GATE, gpio.LOW)
    
while(True):
    resetPins()
    gpio.output(START_DETECTED, gpio.LOW)
    gpio.output(NEW_GATE, gpio.LOW)
    tags = []
    cam = cv2.VideoCapture(0)
    if(cam.isOpened == False):
        sys.exit()
    _,img = cam.read()
    cam.release()
    (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    if(cornerpts == []):
        continue

    for j in range(len(ids)):
        g = gate(cornerpts[j][0], ids[j])
        tags.append(g)           

    tags.sort(key = lambda gate: gate.size, reverse = True)
    
    if(tags[0].ID != START):
        continue;
    
    closestGate = 0;
    gpio.output(START_DETECTED, gpio.HIGH)
    
    while(True):
        cam = cv2.VideoCapture(0)
        if(cam.isOpened == False):
            sys.exit()

        tags = []
        _, img = cam.read()
        cam.release()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)
        
        resetPins()
        
        if(cornerpts == []):
            gpio.output(NO_GATE, gpio.HIGH)
            uart.write("No gates\n")

        else:
            for j in range(len(ids)):
                g = gate(cornerpts[j][0], ids[j])
                tags.append(g)           

            tags.sort(key = lambda gate: gate.size, reverse = True)
            
            if(ids[0] == STOP):
                break;
            
            if((len(ids) >= 2) and ((tags[0].ID == 0 and tags[1].ID == 1 and tags[0].corners[0][0] < tags[1].corners[0][0]) or  (tags[0].ID == 1 and tags[1].ID == 0 and tags[0].corners[0][0] > tags[1].corners[0][0]))):
                if(tags[1].size > 0.75*tags[0].size):
                    if(tags[0].size < closestGate):
                        gpio.output(NEW_GATE, not gpio.input(NEW_GATE))
                    closestGate = tags[0].size
                    
                    target = (tags[0].corners[0][0] + tags[1].corners[1][0]) / 2
                    uart.write('Target: %d, IMGCENTER: %d, Size: %d\n'%(target, imgCenterX, tags[0].size))
                    if(target < 0.4*imgCenterX):
                        gpio.output(HL, gpio.HIGH)
                    elif(0.4*imgCenterX < target < 0.8*imgCenterX):
                        gpio.output(L, gpio.HIGH)
                    elif(0.8*imgCenterX < target < 1.2*imgCenterX):
                        gpio.output(S, gpio.HIGH)
                    elif(1.2*imgCenterX < target < 1.6*imgCenterX):
                        gpio.output(R, gpio.HIGH)
                    elif(1.6*imgCenterX < target):
                        gpio.output(HR, gpio.HIGH)
            else:
                gpio.output(NO_GATE, gpio.HIGH)
                uart.write("No Gates\n")

    gpio.output(START_DETECTED, gpio.LOW)
