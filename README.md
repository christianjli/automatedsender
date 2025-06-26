# Gift Automation

This script automates opening and sending gifts when using **iPhone Mirroring** on macOS Sequoia.

It uses `pyautogui` for input automation, `cv2` for screen color analysis, and `Hammerspoon` (via hotkey + Lua script) to simulate swipe gestures.

## Requirements

- macOS Sequoia with **iPhone Mirroring** enabled
- Hammerspoon (installed + configured)
- Python 3.8+
- Python packages:
  - `pyautogui`, `opencv-python`, `pynput`, `numpy`

## What It Does

1. Opens all available gifts
2. Opens and sends gifts from eligible friends
3. Uses screen region color checks to decide whether a gift can be opened or sent
4. Swipes to the next friend using Hammerspoon hotkey
5. Exits to main page

## How to Use

1. Calibrate the mirrored screen window:
  - Adjust `topleft` and `bottomright` in `main.py` based on your iPhone Mirroring window
  - Use `test.py` to preview and verify coordinates
2. Set up Hammerspoon
  - Create the file `~/.hammerspoon/init.lua`
  - Paste the swipe script from `lua.txt` to simulate a right-to-left swipe gesture
3. Run the script
    ```bash
   python automatedgifts.py
4. Press `Esc` at any time to exit cleanly.

## Warnings

Use responsibly. This is intended for personal automation/testing only.

