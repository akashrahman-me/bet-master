import pyautogui

def find_image_center(image_path, confidence=0.8):
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                x, y = location
                return (x, y)
            else:
                continue
        except pyautogui.ImageNotFoundException:
            continue