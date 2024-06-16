import time
import pyautogui
from PIL import Image
import tempfile
import os
import re
import pytesseract
import random

class CaptureWinnings:
    def __init__(self, width=170, height=56, x=1920 - 200, y=300):
        self.screen_w, self.screen_h = pyautogui.size()
        self.width = width
        self.height = height
        self.x = x
        if x == 0:
            self.x = self.screen_w - width
        self.y = y
        self.helper_winnings1 = None
        self.helper_winnings2 = None

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        # screenshot.show()
        return screenshot

    def save_screenshot(self, screenshot):
        temp_dir = tempfile.gettempdir()
        screenshot_path = os.path.join(temp_dir, f"screenshot_{random.randint(1, 1000)}.png")
        screenshot.save(screenshot_path)
        return screenshot_path

    def extract_text(self, image_path):
        return pytesseract.image_to_string(Image.open(image_path))

    def remove_screenshot(self, image_path):
        if os.path.exists(image_path):
            os.remove(image_path)

    def is_valid_format(self, text):
        return bool(re.match(r'^\d+\.\d+x$', text))
    
    def processing_text(self):
        start_time = time.perf_counter()
        
        screenshot = self.capture_screenshot()
        screenshot_path = self.save_screenshot(screenshot)
        
        text = self.extract_text(screenshot_path)
        self.remove_screenshot(screenshot_path)
        
        elapsed_time = time.perf_counter() - start_time
        # print(f"Time taken: {elapsed_time:.3f}s")

        return text.strip()

    def run(self, target = None):
        valid_text_count = 0
        last_valid_text = None

        while True:
            text = self.processing_text()
            if text and self.is_valid_format(text):
                if text == last_valid_text:
                    valid_text_count += 1
                else:
                    valid_text_count = 1
                    last_valid_text = text
                
                winning_number = float(text.replace('x', ''))

                if target is not None:
                    if winning_number >= target:
                        return winning_number

                if valid_text_count == 5 and last_valid_text != '1.00x':
                    return winning_number
                
            else:
                if last_valid_text != None and last_valid_text == '1.00x':
                    return float(last_valid_text.replace('x', ''))

# Usage
if __name__ == "__main__":
    screen_capture = CaptureWinnings()
    text = screen_capture.run()
    print(text)
