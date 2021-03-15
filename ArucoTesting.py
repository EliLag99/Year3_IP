import cv2
import time

arucoParams = cv2.aruco.DetectorParameters_create()

pixel = input("How many pixels: ")
arucoDict = cv2.aruco.Dictionary_create(4, int(pixel))

print("Opening file...")
file = open("Testing"+pixel+"px.txt", "w")
file.write("###TESTING ARUCOS###")

cam = cv2.VideoCapture(0)
if(cam.isOpened()):
    cam.release()
    print("Starting test for ", pixel, "px tags")
    for i in range(15):
        file.write("\nDistance: " + str(30 + i*15) + "cm\n")
        j = 0
        while j < 4:
            cam = cv2.VideoCapture(0)
            _, img = cam.read()
            cv2.imshow("CurrImg", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cam.release()
            cont = input("Continue? ")
            if(cont != "y"):
                continue
            j+=1
            (cornerpts, ids, rejected) = cv2.aruco.detectMarkers(img, arucoDict, parameters=arucoParams)
            if(cornerpts == []):
                file.write("0\t")
                print("No gate recognized")
            else:
                file.write(str(len(ids)) + "\t")
                print(len(ids), "gate(s) recognized with IDs: ", ids)
        if(i!=14):
            time.sleep(1)
            print("Move camera to next position")
else:
    print("Camera opening failed")
    
print("Finished testing for ", pixel, "px tags")
file.close()
