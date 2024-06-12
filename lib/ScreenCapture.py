import time
import pyautogui
from PIL import Image
import tempfile
import os
import pytesseract

class ScreenCapture:
    def __init__(self, width=170, height=56, x = 0,  y=250):
        self.screen_w, self.screen_h = pyautogui.size()
        self.width = width
        self.height = height
        self.x = x
        if x == 0:
            self.x = self.screen_w - width
        self.y = y

    def capture_screenshot(self):
        screenshot = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        # screenshot.show()
        return screenshot

    def save_screenshot(self, screenshot):
        temp_dir = tempfile.gettempdir()
        screenshot_path = os.path.join(temp_dir, "screenshot.png")
        screenshot.save(screenshot_path)
        return screenshot_path

    def extract_text(self, image_path):
        return pytesseract.image_to_string(Image.open(image_path))

    def remove_screenshot(self, image_path):
        if os.path.exists(image_path):
            os.remove(image_path)

    def run(self):

        start_time = time.monotonic()
        
        screenshot = self.capture_screenshot()
        screenshot_path = self.save_screenshot(screenshot)
        
        text = self.extract_text(screenshot_path)
        self.remove_screenshot(screenshot_path)
        
        elapsed_time = time.monotonic() - start_time
        # print(f"Time taken: {elapsed_time:.3f}s")
        return text.strip()

# Usage
if __name__ == "__main__":
    screen_capture = ScreenCapture()
    text = screen_capture.run()
    print(text)
