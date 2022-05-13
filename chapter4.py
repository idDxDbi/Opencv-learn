import cv2
import numpy as np

"""
画出矩形、圆，学习如何再图像上放置文本
"""

img = np.zeros((512,512,3), np.uint8)

# img[:] = 255,0,0
cv2.line(img, (0,0),(300,300),(0,255,0), 3)
cv2.rectangle(img, (200,100), (300,400),(255,0,0), 2)
cv2.circle(img, (100,100),100,(0,255,0), 3)
cv2.putText(img,"OPENCV",(300,200),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,150,0),2)





cv2.imshow("image", img)

cv2.waitKey(0)