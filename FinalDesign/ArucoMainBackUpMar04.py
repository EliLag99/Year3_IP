import cv2
import time
import serial
from picamera import PiCamera

ARUCO = cv2.aruco.DICT_5X5_50

LEFT_TAG = 3
RIGHT_TAG = 1
START_TAG = 2
STOP_TAG = 0

ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

class gate:
    def __init__(self, corners):
        self.corners = corners
        self.size = abs(corners[0] - corners[1])
        
def middle(corners):
    return(corners[0][0]+corners[1][0]) / 2

arucoDict = cv2.aruco.Dictionary_get(ARUCO)
#arucoDict = cv2.aruco.Dictionary_create(4, 5)
arucoParams = cv2.aruco.DetectorParameters_create()


i=0

cam = cv2.VideoCapture(0)
print(cam.isOpened())
_, img = cam.read()
center = img.shape[0]/2

while(cam.isOpened()):
    left, right = [], []
    _, img = cam.read()
    #cv2.imshow("Prev", img)
    #cv2.waitKey()
    #print(img.shape)
    #time.sleep(5)
    (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
    if(cornerpts == []):
        i+=1
        if(i%10 == 0):
            print(i, "rounds without marker detected")
        if(i > 60):
            print("No gates detected for a while... Stopping")
            break;
    elif(len(ids)==1 and ids[0] == STOP_TAG):
        print("Stop Tag detected... Stopping")
        break
    else:
        i=0
        print(len(ids), '\n')
        for j in range(len(ids)):
            g = gate(cornerpts[j][0])
            
            if(ids[j] == LEFT_TAG):
                left.append(g)
            elif(ids[j] == RIGHT_TAG):
                right.append(g)
            print("Corners:", cornerpts[j][0])
            
            print("ID: ", ids[j])
            ser.write(str.encode("xxx"))            

        #left.sort(key = lambda gate: gate.size, reverse = True)
        #right.sort(key = lambda gate: gate.size, reverse = True)
        if(len(left) != 0 and len(right) != 0):
            target = (middle(left[0].corners) + middle(right[0].corners)) / 2
            print("Left and Right gate recognized, centre: ", target)
        #cv2.destroyAllWindows()

cam.release()