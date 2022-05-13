import cv2
import numpy as np

"""
改变图片大小cv2.resize()
学习如何对图片进行裁剪
"""
img = cv2.imread("../Resources/Lambo.jpeg")
print(img.shape)    #打印出的顺序为（高，宽，BGR）

imgResize = cv2.resize(img, (1000, 500))     #改变图片大小时，格式是（宽，高）
print(imgResize.shape)

imgCropped = img[0:300, 300:600]

cv2.imshow("image", img)
cv2.imshow("Reszie Image", imgResize)
cv2.imshow("Cropped Image", imgCropped)
cv2.waitKey(0)