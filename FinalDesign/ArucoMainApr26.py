import cv2
import sys
import time
import serial
import RPi.GPIO as gpio
from picamera import PiCamera

import UnicornControl as uctrl
import GPIOControl as gctrl

#####SETUP AND CONFIGURATION#####

#Tag IDS
LEFT = 0
RIGHT = 1
START = 2
STOP = 3

#Pin Definitions
HR = 19
R = 13
S = 6
L = 5
HL = 0

START_DETECTED = 10
NO_GATE = 9
NEW_GATE = 11

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
        self.size = abs(corners[0][0] - corners[1][0])

def resetPins():
    gpio.output(HR, gpio.LOW)
    gpio.output(R, gpio.LOW)
    gpio.output(S, gpio.LOW)
    gpio.output(L, gpio.LOW)
    gpio.output(HL, gpio.LOW)
    gpio.output(NO_GATE, gpio.LOW)
    gpio.output(NEW_GATE, gpio.LOW)
    gpio.output(START_DETECTED, gpio.LOW)
    
resetPins()

while(True):
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
    
    gpio.output(START_DETECTED, gpio.HIGH)
    closestGate = 0;
    
    while(True):
        cam = cv2.VideoCapture(0)
        cam.set(3,2592)
        cam.set(4,1944)
        if(cam.isOpened == False):
            sys.exit()

        tags = []
        _, img = cam.read()
        cam.release()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(gray, arucoDict, parameters=arucoParams)
        
        if(cornerpts == []):
            uctrl.noGates()
            gpio.output(NO_GATE, gpio.HIGH)
            uart.write("No gates\n")

        else:
            print(len(ids), '\n')
            print(ids)
            for j in range(len(ids)):
                g = gate(cornerpts[j][0], ids[j])
                tags.append(g)           

            tags.sort(key = lambda gate: gate.size, reverse = True)
            
            if(ids[0] == STOP):
                break;
            
            if((len(ids) >= 2) and ((tags[0].ID == 0 and tags[1].ID == 1) or  (tags[0].ID == 1 and tags[1].ID == 0))):
                size = tags[0].corners[3][1] - tags[0].corners[0][1]
                
                if(size < closestGate):
                    gpio.output(NEW_GATE, not gpio.input(NEW_GATE))
                closestGate = size
                
                target = (tags[0].corners[0][0] + tags[1].corners[1][0]) / 2
                center1 = (int((tags[0].corners[0][0] + tags[0].corners[1][0]) / 2), int((tags[0].corners[0][1] + tags[0].corners[3][1]) / 2))
                center2 = (int((tags[1].corners[0][0] + tags[1].corners[1][0]) / 2), int((tags[1].corners[0][1] + tags[1].corners[3][1]) / 2))
                circle = ((center1[0]+center2[0])/2, (center1[1]+center2[1])/2)
                cv2.line(img,center1,center2,(255,0,0),1)
                cv2.circle(img,circle,5,(0,0,255),5)
                cv2.aruco.drawDetectedMarkers(img, cornerpts, ids)
                cv2.imshow('Image',img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.imwrite("/home/pi/Desktop/IP/path.png",img)
                print("Left and Right gate recognized, centre: ", target, "\tImage center: ", imgCenterX)
                resetPins()
                gpio.output(NO_GATE, gpio.LOW)
                uart.write('Target: %d, IMGCENTER: %d, Size: %d\n'%(target, imgCenterX, size))
                if(target < 0.4*imgCenterX):
                    uctrl.hleft()
                    gctrl.hleft()
                elif(0.4*imgCenterX < target < 0.8*imgCenterX):
                    uctrl.left()
                    gctrl.hleft()
                elif(0.8*imgCenterX < target < 1.2*imgCenterX):
                    uctrl.straight()
                    gctrl.straight()
                elif(1.2*imgCenterX < target < 1.6*imgCenterX):
                    uctrl.right()
                    gctrl.right()
                elif(1.6*imgCenterX < target):
                    uctrl.hright()
                    gctrl.hright()
            else:
                uctrl.noGates()
                gpio.output(NO_GATE, gpio.HIGH)
                uart.write("No Gates\n")

    gpio.output(START_DETECTED, gpio.LOW)
