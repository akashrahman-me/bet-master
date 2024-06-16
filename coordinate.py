import time
import subprocess
from PIL import Image, ImageDraw
import io
import matplotlib.pyplot as plt
import threading

# Function to take a screenshot using ADB
def take_screenshot():
    # Take a screenshot and save it to /sdcard/screen.png on the device
    subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)

    # Pull the screenshot from the device to the local machine
    screenshot = subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE).stdout

    # Load the screenshot into a PIL Image
    image = Image.open(io.BytesIO(screenshot))
    return image

# Function to draw a circle on the image
def draw_circle(image, x, y):
    draw = ImageDraw.Draw(image)
    size = 20
    draw.ellipse([(x - (size / 2), y - (size / 2)), (x + (size / 2), y + (size / 2))], outline='red', width=3)
    return image

# Function to display the image
def display_image(image):
    plt.imshow(image)
    plt.axis('off')  # Hide axes
    plt.show()

# if __name__ == '__main__':
#     screenshot = take_screenshot()
#     x = 917
#     y = 1170
#     image_with_circle = draw_circle(screenshot, x, y)
#     print(f"Center of the circle: {x}x{y}")
#     display_image(image_with_circle)


# Function to simulate a touch event at specific coordinates
def touch_screen(x, y):
    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])

# touch_screen(290, 1350) # Place a Bet

def x():
    touch_screen(800, 1350)

threading.Thread(target=x).start()
 #Take Winning