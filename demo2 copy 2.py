import cv2
import numpy as np

img = cv2.imread("./pic/youyu.jpg")
img2 = cv2.imread("./pic/wuyu.jpg")
img = cv2.GaussianBlur(img, [9, 9], 0)
img2 = cv2.GaussianBlur(img2, [9, 9], 0)
diff = cv2.absdiff(img, img2)
cvtDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
_, result = cv2.threshold(cvtDiff, 20, 255, cv2.THRESH_BINARY)
result = cv2.dilate(result, np.ones([3, 3]))
contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
areas = []
for c in contours:
  areas.append(cv2.contourArea(c))
index = np.argsort(areas)[-5:]
top5_contours = []
for i in range(5):
  top5_contours.append(contours[index[i]])
for c in top5_contours:
  x, y, w, h = cv2.boundingRect(c)
  cv2.rectangle(img2, [x, y], [x + w, y + h], [0, 0, 255], 3)
cv2.imshow("diff", img2)
# cv2.imshow('cvtDiff', cvtDiff)
cv2.imshow("result", result)
cv2.waitKey(0)


class fishing:
  def detect(img1, img2):
    img1 = cv2.GaussianBlur(img1, [9, 9], 0)
    img2 = cv2.GaussianBlur(img2, [9, 9], 0)
    diff = cv2.absdiff(img, img2)
    cvtDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(cvtDiff, 20, 255, cv2.THRESH_BINARY)
    result = cv2.dilate(result, np.ones([3, 3]))
    contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for c in contours:
      areas.append(cv2.contourArea(c))
    index = np.argsort(areas)[-5:]
    top5_contours = []
    for i in range(5):
      top5_contours.append(contours[index[i]])
    rect_pos = []
    for c in top5_contours:
      rect_pos.append(cv2.boundingRect(c))
    return rect_pos
  
