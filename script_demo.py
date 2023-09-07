import cv2
import pyautogui
import time

def get_target_xy(img_path_name):
    pyautogui.screenshot().save('./pic/scrennshot.png')
    img = cv2.imread('./pic/scrennshot.png')
    img_bilibili = cv2.imread('./pic/' + img_path_name)
    height, width, channel = img_bilibili.shape
    result = cv2.matchTemplate(img, img_bilibili, cv2.TM_SQDIFF_NORMED)
    upper_left = cv2.minMaxLoc(result)[2]
    avg = (int(upper_left[0] + width/2), int(upper_left[1] + height/2))
    return avg

def auto_click(var_avg):
    pyautogui.click(var_avg[0], var_avg[1], button='right', duration=1)
    time.sleep(1)


def routine(img_path, name):
    avg = get_target_xy(img_path)
    print(f'正在点击{name}')
    auto_click(avg)
    

# img = cv2.imread('./pic/20230803163237.png')
# draw_0 = cv2.rectangle(img, (50,50), (100,100), (255,0,0), 10)
# cv2.imshow('German', draw_0)
# img = cv2.imread('./pic/scrennshot.png')
# cv2.namedWindow('window', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('window', 800, 600)
# cv2.imshow('window', 0)
# key = cv2.waitKey(0)
# if key == ord('q'):
#     print('destroy')
#     cv2.destroyAllWindows()
routine('20230803163237.png', 'bilibili')