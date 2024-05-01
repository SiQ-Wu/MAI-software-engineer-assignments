import cv2
import numpy as np
import math

def GetOutline(img):
    # 预处理，找图像边缘
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ratio = 750 / img.shape[0] 
    imgGray = cv2.resize(imgGray,(0,0),fx=ratio,fy=ratio)  
    imgGray = cv2.GaussianBlur(imgGray,(3,3),sigmaX=4)
    binary = cv2.adaptiveThreshold(~imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    imgEdge = cv2.Canny(binary,50,200)


    # 提取轮廓
    contours,_ = cv2.findContours(imgEdge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # 对轮廓面积进行排序，面积最大的一定是纸张的轮廓
    contours = sorted(contours,key=cv2.contourArea,reverse=True)
    cv2.drawContours(imgGray,contours,0,(0,0,255),2) 
    
#     cv2.imshow("1",imgGray)
#     cv2.waitKey(0)

    return np.array(contours[0]/ratio,dtype=np.int)

def GetQuadPoint(outline):
    # 获取顶点
    epsilon = 0.01 * cv2.arcLength(outline,True)
    cntApprox = cv2.approxPolyDP(outline,epsilon,closed=True)

    # 区分四个顶点位置，存放顺序从左上角开始，逆时针
    # 按照 x 方向的大小对四个点排序
    cntApprrox = sorted(cntApprox,key=lambda point:point[0][0])

    # 左边两点的高低
    if cntApprox[0][0][1] > cntApprox[1][0][1]:
        temp = list(cntApprox[0][0])
        cntApprox[0][0] = list(cntApprox[1][0])
        cntApprox[1][0] = temp

    # 右边两点的高低
    if cntApprox[2][0][1] < cntApprox[3][0][1]:
        temp = list(cntApprox[2][0])
        cntApprox[2][0] = list(cntApprox[3][0])
        cntApprox[3][0] = temp
    
    return cntApprox
    
def pers_trans(img,quadpoint):
    # 透视变换
    points = np.array(quadpoint,dtype=np.float32).reshape((4,-1))
    width =  np.sqrt((points[0,0] - points[3,0])**2 + (points[0,1] - points[3,1])**2) 
    height =  np.sqrt((points[0,0] - points[2,0])**2 + (points[0,1] - points[2,1])**2) 
    width = int(width)
    height = int(height)
    
    dstPoints = np.array([[0,0],[0,height],[width,height],[width,0]],dtype=np.float32)
    m = cv2.getPerspectiveTransform(points,dstPoints)
    imgPers = cv2.warpPerspective(img,m,(width,height))

    ratio = 700 / imgPers.shape[0] 
    imgPers = cv2.resize(imgPers,(0,0),fx=ratio*1.4,fy=ratio)
    
#     cv2.imshow("1",imgPers)
#     cv2.waitKey(0)
    
    return imgPers

def ImgtoMat(img,row,column):
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.GaussianBlur(imgGray,(3,3),sigmaX=4)
    
    img = cv2.threshold(~imgGray, 128, 255, cv2.THRESH_BINARY)[1]
    
    cv2.imshow("1",img)
    cv2.waitKey(0)
    
    h,w = img.shape
    cellWidth = int(w/column)
    cellHeight = int(h/row)

    x = cellWidth
    y = cellHeight
    cellSquare = cellWidth * cellHeight
    outData = []
    for i in range(1, row ):
        for j in range(1, column ):

            roi = img[y : y + cellHeight, x : x + cellWidth]

            whitePixel = 0

            for m in roi:
                for n in m:
                    if n > 0:
                        whitePixel = whitePixel + 1
                        
           # print(whitePixel)
            
        ###################################################
            if whitePixel > 0.2 * cellSquare:
                outData.append(1)
            else:
                outData.append(0)
            x = x + cellWidth
        x = cellWidth
        y = y + cellHeight
        
    matrix = np.array(outData).reshape(row-1,column-1)
   # print(matrix)
    ####################################
    return matrix

def CheckAnswers(mat1,mat2):
    
    result = []
    wrongAnswers = []
    
    for i in range(0, len(mat1)):
        for j in range(0, len(mat1[1])):
            if mat1[i][j] != mat2[i][j] and (i + 1) not in wrongAnswers:
                wrongAnswers.append(i + 1)
    
    correctRate = round((len(mat1) - len(wrongAnswers)) * 100 / (len(mat1)), 1)
    
    return wrongAnswers, correctRate

if __name__ == '__main__':
    
    # 处理学生表格
    student = cv2.imread('test4.jpg')
   
    Outline = GetOutline(student)
    QuadPoint = GetQuadPoint(Outline)
    student = pers_trans(student,QuadPoint)
    stu_answer = ImgtoMat(student,11,6)
    
#     #处理答案表格
#     answer = cv2.imread('answer3.jpg')
#     answer = ImgtoMat(answer,11,6)

    answer = cv2.imread('answer2.jpg')
   

    Outline2 = GetOutline(answer)
    QuadPoint2 = GetQuadPoint(Outline2)
    answer = pers_trans(answer,QuadPoint2)
    answer = ImgtoMat(answer,11,6)
    
    wrong,rate = CheckAnswers(stu_answer,answer)
    
    print('Student answer:')
    print(stu_answer)
    print('Correct answer:')
    print(answer)
    
    print('The number of the wrong question is:'+str(wrong))
    print('Correct Rate:'+str(rate)+'%')
