import cv2

img = cv2.imread("img.png")

(cornerpts, ids, rejected) = cv2.aruco.detectMarkers(img, cv2.aruco.Dictionary_create(4, 2), parameters=cv2.aruco.DetectorParameters_create())

print(cornerpts)