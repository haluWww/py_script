import cv2
import numpy as np 

img = cv2.imread('./pic/youyu.jpg')
img2 = cv2.imread('./pic/wuyu.jpg')
img = cv2.GaussianBlur(img, [9, 9], 0)
img2 = cv2.GaussianBlur(img2, [9, 9], 0)
diff = cv2.absdiff(img, img2)
cvtDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, result = cv2.threshold(cvtDiff, 20, 255,  cv2.THRESH_BINARY)
result = cv2.dilate(result, np.ones([3,3]))
c_x = int(result.shape[1] / 2)
c_y = int(result.shape[0] / 2)
cv2.imshow('diff', result)
result = result[c_y - 70:c_y + 20, c_x - 10:c_x + 10]
contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow('cvtDiff', cvtDiff)
cv2.imshow('result', result)
cv2.waitKey(0)