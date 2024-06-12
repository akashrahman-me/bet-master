import easyocr
from PIL import Image, ImageEnhance, ImageFilter
import re
import os
import tempfile
from lib.ScreenCapture import ScreenCapture

class StatusExtractor:
    def __init__(self, width=420, height=64, x=1920 - 200, y=300):
        # Fine Tune
        self.width = width
        self.height = height
        self.x = x - 250
        self.y = y + 345
        self.screen_capture = ScreenCapture(self.width, self.height, self.x, self.y)
        self.screenshot_path = None
        self.reader = easyocr.Reader(['en'])

    def capture_screenshot(self):
        screenshot = self.screen_capture.capture_screenshot()
        self.screenshot_path = self.screen_capture.save_screenshot(screenshot)
        return self.screenshot_path

    def process_image(self, image_path):
        # Open the image
        image = Image.open(image_path)

        # Resize the image to improve resolution (optional)
        image = image.resize((image.width * 1, image.height * 1), Image.Resampling.LANCZOS)

        # Convert to grayscale
        gray_image = image.convert('L')

        # Enhance the image contrast
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(1)

        # Apply a sharpening filter
        sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)
        # sharpened_image.show()

        # Save the processed image temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        sharpened_image.save(temp_file.name)
        return temp_file.name

    def extract_text(self, processed_image_path):
        # Read the text from the processed image
        results = self.reader.readtext(processed_image_path, detail=0)

        # Join results into a single string
        text = ' '.join(results)
        return text

    def extract_digits(self, text):
        # Extract only digits and spaces
        digits_text = re.findall(r'\d+\.\d+|\d+', text)
        return digits_text

    def format_data(self, digits_text):
        # Convert to appropriate types and format
        data = {
            "players": int(digits_text[0]) if len(digits_text) > 0 else 0,
            "bets": float(digits_text[1]) if len(digits_text) > 1 else 0.0,
            "winnings": float(digits_text[-1]) if len(digits_text) > 2 else 0.0
        }
        return data

    def run(self):
        screenshot_path = self.capture_screenshot()
        processed_image_path = self.process_image(screenshot_path)
        try:
            text = self.extract_text(processed_image_path)
            digits_text = self.extract_digits(text)
            data = self.format_data(digits_text)
        finally:
            os.remove(processed_image_path)  # Ensure the temporary file is deleted
        return data

# Usage
if __name__ == '__main__':
    text_extractor = StatusExtractor()
    data = text_extractor.run()
    print(data)
