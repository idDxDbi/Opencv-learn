import cv2

import numpy as np

"""
检测图像当中车辆的颜色


#练习上一张的知识点
imgStack = function.stackImage(0.5, ([img, imgHSV]))
cv2.imshow("Original", imgStack)


"""


def empty(a):
    pass


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

path = ("../Resources/lambo.jpeg")

cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBar", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBar", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBar", 191, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBar", 255, 255, empty)


while True:
    img = cv2.imread(path)
    #       HSV色彩空间转换
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_Min = cv2.getTrackbarPos("Hue Min", "TrackBar")
    h_Max = cv2.getTrackbarPos("Hue Max", "TrackBar")
    s_Min = cv2.getTrackbarPos("Sat Min", "TrackBar")
    s_Max = cv2.getTrackbarPos("Sat Max", "TrackBar")
    v_Min = cv2.getTrackbarPos("Val Min", "TrackBar")
    v_Max = cv2.getTrackbarPos("Val Max", "TrackBar")
    print(h_Min, h_Max, s_Min, s_Max, v_Min, v_Max)

    lower = np.array([h_Min, s_Min, v_Min])
    upper = np.array([h_Max, s_Max, v_Max])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow("Original", img)
    # cv2.imshow("HSV", imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    imgStack = stackImage(0.5, ([img, imgHSV],[mask, imgResult]))
    cv2.imshow("Stack Image", imgStack)
    cv2.waitKey(1)