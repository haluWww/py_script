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
      
class checkIn:
  f = open('config.json', encoding='utf-8')
  data = json.load(f)
  f.close()
  open = False
  def __init__(self) -> None:
    hour = time.localtime(self.data['inTime']).tm_hour
    self.getWindow()
    if 8 < hour and hour < 12:
      self.qianru()
    else:
      self.qianchu()
      
  def getWindow(self):
    hwnd = 0
    while hwnd == 0:
      time.sleep(1)
      print('找窗口')
      hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
      if self.open == False and hwnd == 0:
        print('打开窗口')
        self.open = True
        webbrowser.open(self.data['om'])
        hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', '腾讯外包研发管理平台 - Google Chrome')
        
      if hwnd != 0:
        print('找到窗口', hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, int(self.data['resolution'][0]), int(self.data['resolution'][1]), win32con.SWP_SHOWWINDOW)
    return hwnd
  def find(self, target):
    pyautogui.screenshot(region=[0, 0, self.data['resolution'][0], self.data['resolution'][1]]).save('./pic/scrennshot.png')
    img = cv2.imread('./pic/scrennshot.png')
    w, h = target.shape[:-1]
    targetResult = cv2.matchTemplate(img, target, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(targetResult)
    return (min_val < 0.01, min_loc, w, h)
  def click(self, loc, w, h):
    print('触发点击')
    pyautogui.click(x=(loc[0] + h/2), y=(loc[1] + w/2), duration=2)
    
    
  def qianru(self):
    self.data['inTime'] = time.time()
    with open('config.json', 'w', encoding='utf-8') as f:
      f.write(json.dumps(self.data))
    flag = self.clickAndNext(cv2.imread('./pic/qianru.png'))
    if flag:
      self.clickAndNext(cv2.imread('./pic/queding.png'))
      
  def qianchu(self):
    self.data['outTime'] = time.time()
    with open('config.json', 'w', encoding='utf-8') as f:
      f.write(json.dumps(self.data))
    flag = self.clickAndNext(cv2.imread('./pic/qianchu.png'))
    if flag:
      self.clickAndNext(cv2.imread('./pic/queding.png'))
      
  def yanzhengma(self):
    ocr = ddddocr.DdddOcr()
    cuowu = cv2.imread('./pic/cuowu.png')
    flag, loc, w, h = self.find(cuowu)
    pyautogui.moveTo(loc[0] + 20, loc[1] - 20)
    pyautogui.screenshot(region=[loc[0] + 264, loc[1] - 74, 245, 63]).save('./pic/ddddocr.png')
    f =  open('./pic/ddddocr.png', mode='rb')
    i = f.read()
    re = ocr.classification(i)
    return re
  
  def clickAndNext(self, target):
    start = time.time()
    end = time.time()
    while (end - start) < 10000:
      time.sleep(1)
      flag, loc, w, h = self.find(target)
      print('找点击目标')
      if flag:
        print('找到目标', loc, w, h)
        self.click(loc, w, h)
        return True;
      end = time.time()
    return False;

checkIn()