import cv2

cam = cv2.VideoCapture(0)

_, img = cam.read()

print(img.shape[0]/2)

cam.release()