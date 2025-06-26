import cv2
import pyautogui
from pynput import keyboard
import time
import numpy as np
import subprocess

def take_screenshot(x, y, w, h, filename='latest_screen.png'):
    '''Take screenshot for image processing.'''
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, screen)
    return screen

def get_window_rect(topleft, bottomright):
    '''Get window coordinates.'''
    x, y = topleft
    w = bottomright[0] - x
    h = bottomright[1] - y
    return x, y, w, h

def click(x_percent, y_percent, rect, delay=0.5):
    x, y, w, h = rect
    click_x = int(x + w * x_percent)
    click_y = int(y + h * y_percent)
    pyautogui.moveTo(click_x, click_y, duration=0.1)
    # pyautogui.click()
    time.sleep(delay)

# Use calibrate.py to find window coordinates
topleft = [5, 80]
bottomright = [338, 790]
GIFT_OPEN_COLOR_THRESHOLD = 723
GIFT_SEND_COLOR_THRESHOLD = 654

# Get window coordinates
window_x, window_y, window_w, window_h = get_window_rect(topleft, bottomright)

pyautogui.moveTo(170, 150, duration=0.1) # click on send gift

rect = get_window_rect(topleft, bottomright)
click(170 / 338, 745 / 790, rect, 0.5) # test coordinates

screen = take_screenshot(*rect)
h, w, _ = screen.shape
top = int(h * 540 / 710)
bottom = int(h * 585 / 710)
left = int(w * 45 / 333)
right = int(w * 85 / 333)
# cv2.imshow("screen", screen[top:bottom, left:right]) # check used region
# cv2.waitKey()
# time.sleep(10)
print(screen[top:bottom, left:right].mean(axis=(0, 1)).sum()) # test recognition of gift availability
print(screen[top:bottom, left:right].mean(axis=(0, 1)).sum() <= GIFT_SEND_COLOR_THRESHOLD)