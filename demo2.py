import cv2
import numpy as np 

# data = np.array([1,2,3,4,5,6,7])
# print(data)

img = cv2.imread('./pic/scrennshot.png')
img = img.astype(np.float16)
img2 = cv2.imread('./pic/20230803163237.png')
# img3 = cv2.imread('./pic/wuyu.jpg')
# index = img3 == np.array([[157, 151, 115], [157, 151, 115], [157, 151, 115]])
# print(index)
c_x = int(img.shape[1] / 2)
c_y = int(img.shape[0] / 2)
img[c_y:c_y+img2.shape[0], c_x:c_x+img2.shape[1], :] += img2
index = img >= 255
img[index] = 255
img = img.astype(np.uint8)
cvtImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
contours, _ = cv2.findContours(cvtImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
areas = []
for c in contours:
    area = cv2.contourArea(c)
    areas.append(area)
print(len(contours))
for c in contours:
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img, [x,y], [x+50, y+50], [0,0,255], 3)
img = cv2.resize(img, (0, 0), fx=1, fy=1)
cv2.imshow('bilibili', img)
cv2.waitKey(0)