import cv2
import numpy as np 

img = cv2.imread('./img/wuyu2.jpg')
img2 = cv2.imread('./img/wuyu1.jpg')

img = cv2.GaussianBlur(img, [9, 9], 0)
img2 = cv2.GaussianBlur(img2, [9, 9], 0)
diff = cv2.absdiff(img, img2)
cvtDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, result = cv2.threshold(cvtDiff, 20, 255,  cv2.THRESH_BINARY)
result = cv2.erode(result, np.ones([5,5]))
c_x = int(result.shape[1] / 2)
c_y = int(result.shape[0] / 2)
# cv2.imshow('diff', result)
result = result[c_y - 80:c_y - 40, c_x - 10:c_x + 10]
contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(contours)
cv2.imshow('result', result)
cv2.waitKey(0)