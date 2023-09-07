import cv2
import numpy as np
import tkinter as tk
import win32gui
import win32con
import pyautogui

class fishing:
  def detect(img1, img2):
    img1 = cv2.GaussianBlur(img1, [1, 1], 0)
    img2 = cv2.GaussianBlur(img2, [1, 1], 0)
    diff = cv2.absdiff(img1, img2)
    cvtDiff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, result = cv2.threshold(cvtDiff, 20, 255, cv2.THRESH_BINARY)
    result = cv2.dilate(result, np.ones([1, 1]))
    contours, _ = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    areas = []
    for c in contours:
      areas.append(cv2.contourArea(c))
    index = np.argsort(areas)[-1:]
    top5_contours = []
    for i in range(1):
      top5_contours.append(contours[index[i]])
    rect_pos = []
    for c in top5_contours:
      rect_pos.append(cv2.boundingRect(c))
    return rect_pos
  
  def painting(target, rect_pos):
    for x, y, w, h in rect_pos:
      cv2.rectangle(target, [x, y], [x + w, y + h], [0, 0, 255], 2)
    

def 搞个图片():
  # hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', "2023最新OpenCV-Python基础教程：2小时实战打造'找茬游戏'辅助工具 | Shady的混乱空间 #python #opencv #编程 - YouTube - Google Chrome")
  hwnd = win32gui.FindWindow('MSPaintApp', '新建 BMP 图像.png - 画图')
  if hwnd != 0:
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0,0,1024,768, win32con.SWP_SHOWWINDOW)
    img = pyautogui.screenshot(region=[0, 0, 1024, 768])
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    moyu = img[228:465, 55: 256, :]
    xiaban = img[228:465, 293: 494, :]
    fish = fishing
    rect_pos = fish.detect(moyu, xiaban)
    fish.painting(moyu, rect_pos)
    cv2.imshow('moyu', moyu)
    cv2.waitKey(0)

root_window = tk.Tk() 
root_window.title('抢手机')
root_window.geometry('200x200+1200+0')
button = tk.Button(root_window, text='下班', width=20, height=2, command=搞个图片)
button.pack()
root_window.mainloop()