import cv2
import numpy as np
import tkinter as tk
import win32gui
import win32con
import pyautogui
import time
import webbrowser
import json
import ddddocr
# ocr = ddddocr.DdddOcr()
# with open('./pic/企业微信截图_16945067071677.png', mode='rb') as f:
#   i = f.read()
#   re = ocr.classification(i)
#   print(re)
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
      
class checkIn:
  data = json.load(open('config.json', encoding='utf-8'))
  def __init__(self) -> None:
    self.getWindow()
    steps = ['qianru', 'queding', 'qianchu', 'queding']
    target = np.array()
    if not self.data['inTime']:
      target = cv2.imread('./pic/qianru.png') 
    else:
      target = cv2.imread('./pic/qianchu.png')
      
    start = time.time()
    end = time.time()
    while (end - start) < 10000:
      time.sleep(1)
      flag, loc, w, h = self.find(target)
      if flag:
        self.click(loc, w, h)
      end = time.time()
        
  def getWindow(self):
    hwnd = 0
    while hwnd == 0:
      time.sleep(1)
      hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
      if hwnd == 0:
        webbrowser.open(self.data['om'])
        time.sleep(2)
        hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
      
      if hwnd != 0:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, int(self.data['resolution'][0]), int(self.data['resolution'][1]), win32con.SWP_SHOWWINDOW)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    return hwnd
  def find(self, target):
    pyautogui.screenshot(region=[0, 0, int(self.data['resolution'][0]), int(self.data['resolution'][1])]).save('./pic/scrennshot.png')
    img = cv2.imread('./pic/scrennshot.png')
    w, h = target.shape[:-1]
    targetResult = cv2.matchTemplate(img, target, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(targetResult)
    return (min_val < 0.01, min_loc, w, h)
  def click(loc, w, h):
    pyautogui.click(x=(loc[0] + h/2), y=(loc[1] + w/2), duration=2)
  def qianru(self):
    qianru = cv2.imread('./pic/qianru.png')
    flag, loc, w, h = self.find(qianru)
    if (flag):
      self.click(loc, w, h)
  def qianchu(self):
    qianchu = cv2.imread('./pic/qianchu.png')
    flag, loc, w, h = self.find(qianchu)
    if (flag):
      self.click(loc, w, h)
  def yanzhengma():
    ocr = ddddocr.DdddOcr()
    f =  open('./pic/企业微信截图_16945067071677.png', mode='rb')
    i = f.read()
    re = ocr.classification(i)
    return re

daka = checkIn()
    
# data = json.load(open('config.json', encoding='utf-8')) 
# def 搞个图片(targetImg):
#   def 点击目标():
#     time.sleep(2)
#     hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
#     if hwnd == 0:
#       webbrowser.open(data['om'])
#       time.sleep(2)
#       hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
      
#     win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, int(data['resolution'][0]), int(data['resolution'][1]), win32con.SWP_SHOWWINDOW)
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    
#     pyautogui.screenshot(region=[0, 0, int(data['resolution'][0]), int(data['resolution'][1])]).save('./pic/scrennshot.png')
#     img = cv2.imread('./pic/scrennshot.png')
#     w, h = targetImg.shape[:-1]
#     targetResult = cv2.matchTemplate(img, targetImg, cv2.TM_SQDIFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(targetResult)
#     if (min_val < 0.01):
#       pyautogui.click(x=(min_loc[0] + h/2), y=(min_loc[1] + w/2), duration=2)
#     else:
#       return
#     time.sleep(2)
    
#     pyautogui.screenshot(region=[0, 0, int(data['resolution'][0]), int(data['resolution'][1])]).save('./pic/scrennshot.png')
#     img = cv2.imread('./pic/scrennshot.png')
#     queding = cv2.imread('./pic/queding.png')
#     w, h = queding.shape[:-1]
#     quedingResult = cv2.matchTemplate(img, queding, cv2.TM_SQDIFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(quedingResult)
#     if (min_val < 0.01):
#       pyautogui.click(x=(min_loc[0] + h/2), y=(min_loc[1] + w/2), duration=2)
#     else:
#       return
#   return 点击目标


  
# root_window = tk.Tk() 
# root_window.title('自动点打卡')
# root_window.geometry('200x200+1200+0')

# qianchu = cv2.imread('./pic/qianchu.png')
# xiaban = tk.Button(root_window, text='下班', width=20, height=2, command=搞个图片(qianchu))
# xiaban.pack()

# qianru = cv2.imread('./pic/qianru.png')
# shangban = tk.Button(root_window, text='上班', width=20, height=2, command=搞个图片(qianru))
# shangban.pack()

# root_window.mainloop()