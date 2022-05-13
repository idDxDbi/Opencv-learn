import cv2
import numpy as np

"""
DOCUMENT SCANNER
文件扫描
"""
##########################
widthImg = 480
heightImg = 640
scale = 0.5
############################

webcam = True
cap = cv2.VideoCapture(1)
cap.set(10, 100)
cap.set(3, 640)
cap.set(4, 480)
path = "../Resources/paper.jpg"


def preProcessing(img):
    imgGray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel,iterations=1)

    return imgThres





def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxArea = 0
    biggest = np.array([])
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)  # 只显示出最大面积的拐角点
    return biggest

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4,1,2), np.int32)
    add = myPoints.sum(1)
    # print("add", add)

    # 对myPoints中的一维列表从小到大进行排序
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("newPoint", myPointsNew)

    return myPointsNew


def getWarp(img, biggest):
    biggest = reorder(biggest)
    print(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20, 20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped, (widthImg, heightImg))

    return imgCropped

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
                    imgArray[x][y] = cv2.resize(imgArray[x][y],
                                                (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
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
                imgArray[x] = cv2.resize(imgArray[x],
                                         (imgArray[0].shape[1], imgArray[0].shape[0]),
                                         None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_BAYER_BG2BGR)
        hor = np.hstack(imgArray)
        ver = hor

    return ver



while True:
    if webcam:
        success, img = cap.read()

    else:
        img = cv2.imread(path)
    img = cv2.resize(img, (widthImg, heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)

    biggest = getContours(imgThres)
    #增加一个判断如果纸张没有出现再摄像头中的话，就不会输出
    if biggest.size != 0:
        # print(biggest)
        imgWarp = getWarp(img, biggest)
        imgArray = [[img, imgThres], [imgContour, imgWarp]]
    else:
        imgArray = [[img, imgThres], [img, img]]

    # cv2.imshow("Result", imgWarp)
    imgStack = stackImage(0.5,imgArray)
    cv2.imshow("stack Image", imgStack)
    # cv2.imshow("Result", imgWarp)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break