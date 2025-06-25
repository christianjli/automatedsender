import cv2
import pyautogui
from pynput import keyboard
import time
import numpy as np
import subprocess
from pynput import keyboard

# Define ESC key handler
should_exit = False
def on_press(key):
    global should_exit
    if key == keyboard.Key.esc:
        should_exit = True
        print("\nQuitting Program")

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

def trigger_swipe():
    # Send Cmd+Option+Ctrl+S key combo to macOS
    applescript = '''
    tell application "System Events"
        key down {command, option, control}
        keystroke "s"
        key up {command, option, control}
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])

def get_window_rect(topleft, bottomright):
    '''Get window coordinates.'''
    x, y = topleft
    w = bottomright[0] - x
    h = bottomright[1] - y
    return x, y, w, h

def take_screenshot(x, y, w, h, filename='latest_screen.png'):
    '''Take screenshot for image processing.'''
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, screen)
    return screen

# Use calibrate.py to find window coordinates
topleft = [5, 80]
bottomright = [338, 790]

# Get window coordinates
window_x, window_y, window_w, window_h = get_window_rect(topleft, bottomright)

pyautogui.moveTo(50, 735, duration=0.1) # go to profile
pyautogui.click() # click on iphone mirroring
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(290, 740, duration=0.1) # click on sort order
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(290, 450, duration=0.1) # click random so we don't flip order
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(290, 740, duration=0.1) # click on sort order
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(290, 630, duration=0.1) # click on can open gift
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(170, 300, duration=0.1) # click on first friend
time.sleep(0.5)
pyautogui.click()
time.sleep(0.5) # load first friend

opened_all_gifts = False
while not opened_all_gifts and not should_exit:
    screen = take_screenshot(window_x, window_y, window_w, window_h)
    roi = screen[490:520, 20:300]  # Region of interest
    mean_color = roi.mean(axis=(0, 1))  # Average over rows and columns

    if mean_color.sum() > 723: # determine if a gift can be opened
        print("Completed Opening Gifts")
        opened_all_gifts = True

    else:
        pyautogui.moveTo(180, 520, duration=0.1) # click on gift
        time.sleep(1)
        pyautogui.click()
        time.sleep(1.5)

        pyautogui.moveTo(295, 695, duration=0.1) # click pin
        time.sleep(1)
        pyautogui.click()

        pyautogui.moveTo(170, 695, duration=0.1) # click open
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)

        pyautogui.moveTo(170, 745, duration=0.1) # quick exit
        pyautogui.click()
        time.sleep(0.5)

        trigger_swipe() # swipe to next friend
        time.sleep(2)

pyautogui.moveTo(170, 745, duration=0.1) # quick exit
pyautogui.click()
time.sleep(0.5)

pyautogui.moveTo(290, 740, duration=0.1) # click on sort order
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(290, 685, duration=0.1) # click on can open gift
time.sleep(0.5)
pyautogui.click()

pyautogui.moveTo(170, 300, duration=0.1) # click on first friend
time.sleep(0.5)
pyautogui.click()
time.sleep(1.5) # load first friend

sent_all_gifts = False
while not sent_all_gifts and not should_exit:
    screen = take_screenshot(window_x, window_y, window_w, window_h)
    roi = screen[540:585, 45:85]  # Region of interest
    mean_color = roi.mean(axis=(0, 1))  # Average over rows and columns

    if mean_color.sum() > 654:
        print("Completed Sending Gifts")
        sent_all_gifts = True

    else:
        pyautogui.moveTo(70, 650, duration=0.1) # click on send gift
        time.sleep(0.5)
        pyautogui.click()

        pyautogui.moveTo(180, 530, duration=0.1) # click on gift
        time.sleep(0.5)
        pyautogui.click()

        pyautogui.moveTo(170, 695, duration=0.1) # click on send
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(1)

        pyautogui.moveTo(170, 745, duration=0.1) # quick exit
        pyautogui.click()
        time.sleep(0.5)

        trigger_swipe() # swipe to next friend
        time.sleep(2)

if not should_exit:
    pyautogui.moveTo(170, 745, duration=0.1) # exit
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)

else:
    print("Quitting")