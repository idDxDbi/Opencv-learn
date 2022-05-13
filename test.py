import cv2
import numpy as np

img = cv2.imread("../Resources/lena.png")
imgArray = [[img, img, img],
            [img, img, img]]
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgGray2 = cv2.resize(imgGray, (0, 0))
# if len(imgArray[0][0]) == 2: imgArray[0][0] =

print(img.shape)
print(imgArray[0][0].shape)
print(imgGray.shape)
print(imgArray[1])

cv2.imshow("img", imgGray2)
cv2.waitKey(0)
