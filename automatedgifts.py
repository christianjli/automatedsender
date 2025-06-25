import cv2
import pyautogui
from pynput import keyboard
import time
import numpy as np
import subprocess
from pynput import keyboard

# ========== Constants ==========
topleft = [5, 80]
bottomright = [338, 790]
GIFT_OPEN_COLOR_THRESHOLD = 723
GIFT_SEND_COLOR_THRESHOLD = 654

# ========== Exit Flag via ESC ==========
should_exit = False
def on_press(key):
    global should_exit
    if key == keyboard.Key.esc:
        should_exit = True
        print("\nQuitting Program")
keyboard.Listener(on_press=on_press).start()

# ========== Utilities ==========
def click(x, y, delay=0.5):
    pyautogui.moveTo(x, y, duration=0.1)
    pyautogui.click()
    time.sleep(delay)

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
    x, y = topleft
    w = bottomright[0] - x
    h = bottomright[1] - y
    return x, y, w, h

def take_screenshot(x, y, w, h, filename='latest_screen.png'):
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, screen)
    return screen

def get_roi_sum(screen, top, bottom, left, right):
    roi = screen[top:bottom, left:right]
    return roi.mean(axis=(0, 1)).sum()

# ========== Setup App ==========
def setup_app():
    click(50, 735)   # iPhone mirror focus
    click(50, 735)   # Profile
    click(290, 740)  # Sort
    click(290, 450)  # Random sort
    click(290, 740)  # Sort again
    click(290, 630)  # Can open gift
    click(170, 300)  # First friend
    time.sleep(0.5) # Wait to load

# ========== Open All Gifts ==========
def open_all_gifts(rect):
    print("Opening gifts...")
    while not should_exit:
        screen = take_screenshot(*rect)
        if get_roi_sum(screen, 490, 520, 20, 300) > GIFT_OPEN_COLOR_THRESHOLD:
            print("Completed Opening Gifts")
            break
        click(180, 520, 1)   # Gift
        click(295, 695, 1)   # Pin
        click(170, 695, 1)   # Open
        click(170, 745, 0.5) # Quick exit
        trigger_swipe() # Next
        time.sleep(2) # Load
    click(170, 745) # Exit

# ========== Send All Gifts ==========
def send_all_gifts(rect):
    print("Sending gifts...")
    click(290, 740) # Sort
    click(290, 685) # Can send gift
    click(170, 300) # First friend
    time.sleep(1.5) # Wait to load

    while not should_exit:
        screen = take_screenshot(*rect)
        if get_roi_sum(screen, 540, 585, 45, 85) > GIFT_SEND_COLOR_THRESHOLD:
            print("Completed Sending Gifts")
            break
        click(70, 650, 0.5)   # Send gift
        click(180, 530, 0.5)  # Pick gift
        click(170, 695, 0.5)  # Send
        click(170, 745, 0.5)  # Quick exit
        trigger_swipe()
        time.sleep(2)

# ========== Main ==========
def main():
    rect = get_window_rect(topleft, bottomright)
    setup_app()
    open_all_gifts(rect)
    send_all_gifts(rect)

    if not should_exit:
        click(170, 745, 0.5) # Exit
        click(170, 745, 0.5)
    else:
        print("Quitting")

if __name__ == "__main__":
    main()