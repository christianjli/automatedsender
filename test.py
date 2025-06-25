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

# Use calibrate.py to find window coordinates
topleft = [5, 80]
bottomright = [338, 790]

# Get window coordinates
window_x, window_y, window_w, window_h = get_window_rect(topleft, bottomright)

pyautogui.moveTo(290, 450, duration=0.1) # click on send gift
time.sleep(0.5)