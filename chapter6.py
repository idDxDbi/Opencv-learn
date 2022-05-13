import cv2
import numpy as np
"""
将图片组合在一起
"""
img1 = cv2.imread("../Resources/lena.png")
img2 = cv2.imread("../Resources/Lambo.jpeg")
imgGray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
# #水平组合
# imgHor = np.hstack((imgGray,imgGray))
# imgHor = np.hstack((img1,img2))
# #垂直组合
# imgVer = np.vstack((img1,img1))
#这两种函数都不能改变图片大小，并且是要相同GBR、一样大小的图片才能组合


#解决方案
def stackImage(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_BAYER_BG2BGR)
        imageBlank = np.zeros((width,height,3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_BAYER_BG2BGR)
        hor = np.hstack(imgArray)
        ver = hor

    return ver
imgStack =stackImage(0.5,([img1, imgGray, img2], [img1, img1, img1]))


cv2.imshow("imageStack", imgStack)
# cv2.imshow("Horizontal", imgHor)
# cv2.imshow("Vertical", imgVer)
cv2.waitKey(0)
