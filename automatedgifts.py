import cv2
import pyautogui
from pynput import keyboard
import time
import numpy as np
import subprocess

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
def click(x_percent, y_percent, rect, delay=0.5):
    x, y, w, h = rect
    click_x = int(x + w * x_percent)
    click_y = int(y + h * y_percent)
    pyautogui.moveTo(click_x, click_y, duration=0.1)
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

def gift_available(screen):
    h, w, _ = screen.shape
    top = int(h * 490 / 710)
    bottom = int(h * 520 / 710)
    left = int(w * 20 / 333)
    right = int(w * 300 / 333)
    return screen[top:bottom, left:right].mean(axis=(0, 1)).sum() <= GIFT_OPEN_COLOR_THRESHOLD

def send_available(screen):
    h, w, _ = screen.shape
    top = int(h * 540 / 710)
    bottom = int(h * 585 / 710)
    left = int(w * 45 / 333)
    right = int(w * 85 / 333)
    return screen[top:bottom, left:right].mean(axis=(0, 1)).sum() <= GIFT_SEND_COLOR_THRESHOLD

# ========== Setup App ==========
def setup_app(rect):
    click(50 / 338, 735 / 790, rect)   # iPhone mirror focus
    click(50 / 338, 735 / 790, rect)   # Profile
    click(165 / 338, 70 / 790, rect)  # Friends list
    click(290 / 338, 740 / 790, rect)  # Sort
    click(290 / 338, 420 / 790, rect)  # Random sort
    click(290 / 338, 740 / 790, rect)  # Sort again
    click(290 / 338, 615 / 790, rect)  # Can open gift
    click(170 / 338, 270 / 790, rect)  # First friend
    time.sleep(0.5) # Wait to load

# ========== Open All Gifts ==========
def open_all_gifts(rect):
    print("Opening gifts...")
    while not should_exit:
        screen = take_screenshot(*rect)
        if not gift_available(screen):
            print("Completed Opening Gifts")
            break
        click(180 / 338, 480 / 790, rect, 1.5)   # Gift
        click(295 / 338, 680 / 790, rect, 1)   # Pin
        click(170 / 338, 680 / 790, rect, 1.5)   # Open
        click(170 / 338, 745 / 790, rect, 0.5) # Quick exit
        trigger_swipe() # Next
        time.sleep(2) # Load
    click(170 / 338, 745 / 790, rect) # Exit

# ========== Send All Gifts ==========
def send_all_gifts(rect):
    print("Sending gifts...")
    click(290 / 338, 740 / 790, rect) # Sort
    click(290 / 338, 685 / 790, rect) # Can send gift
    click(170 / 338, 270 / 790, rect) # First friend
    time.sleep(1.5) # Wait to load

    while not should_exit:
        screen = take_screenshot(*rect)
        if gift_available(screen):
            click(170 / 338, 745 / 790, rect, 0.5) # Exit
            time.sleep(1)
            continue
        if not send_available(screen):
            print("Completed Sending Gifts")
            break
        click(70 / 338, 630 / 790, rect, 0.5)   # Send gift
        click(180 / 338, 510 / 790, rect, 0.5)  # Pick gift
        click(170 / 338, 675 / 790, rect, 1.0)  # Send
        click(170 / 338, 745 / 790, rect, 0.5)  # Quick exit
        trigger_swipe()
        time.sleep(2)

# ========== Main ==========
def main():
    rect = get_window_rect(topleft, bottomright)
    setup_app(rect)
    open_all_gifts(rect)
    send_all_gifts(rect)

    if not should_exit:
        click(170 / 338, 745 / 790, rect, 0.5) # Exit
        click(170 / 338, 745 / 790, rect, 0.5)
    else:
        print("Quitting")

if __name__ == "__main__":
    main()