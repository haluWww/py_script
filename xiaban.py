import cv2
import numpy as np
import tkinter as tk
import win32gui
import win32con
import pyautogui
import time
import webbrowser

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
  time.sleep(2)
  hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
  if hwnd == 0:
    webbrowser.open('https://om.tencent.com/attendances/check_out/20950700?from=TAPD')
    time.sleep(2)
    hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
    
  win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0,0,2560,1440, win32con.SWP_SHOWWINDOW)
  win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
  pyautogui.screenshot(region=[0,0,2560,1440]).save('./pic/scrennshot.png')
  img = cv2.imread('./pic/scrennshot.png')
  qianchu = cv2.imread('./pic/qianchu.png')
  w, h = qianchu.shape[:-1]
  qianchuResult = cv2.matchTemplate(img, qianchu, cv2.TM_SQDIFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(qianchuResult)
  pyautogui.click(x=(min_loc[0] + h/2), y=(min_loc[1] + w/2), duration=2)
  
  time.sleep(2)
  
  pyautogui.screenshot(region=[0,0,2560,1440]).save('./pic/scrennshot.png')
  img = cv2.imread('./pic/scrennshot.png')
  queding = cv2.imread('./pic/queding.png')
  w, h = queding.shape[:-1]
  quedingResult = cv2.matchTemplate(img, queding, cv2.TM_SQDIFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(quedingResult)
  pyautogui.click(x=(min_loc[0] + h/2), y=(min_loc[1] + w/2), duration=2)

  
root_window = tk.Tk() 
root_window.title('抢手机')
root_window.geometry('200x200+1200+0')
xiaban = tk.Button(root_window, text='下班', width=20, height=2, command=搞个图片)
xiaban.pack()
shangban = tk.Button(root_window, text='上班', width=20, height=2, command=搞个图片)
shangban.pack()
root_window.mainloop()