import tkinter as tk

class ScreenOverlay:
    def __init__(self, width=170, height=56, x=1920 - 200, y=300):
        self.root = tk.Tk()
        self.root.attributes("-transparentcolor", "blue")  # Make blue color transparent
        self.root.attributes("-topmost", True)  # Keep the window on top
        self.root.overrideredirect(True)  # Remove window decorations
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="blue")
        self.canvas.pack()
        
        self.canvas.create_rectangle(0, 0, width, height, outline="red", width=2)
        
        # Schedule the window to be destroyed after 1 second (1000 milliseconds)
        # self.root.after(500, self.destroy_overlay)
        
    def destroy_overlay(self):
        self.root.destroy()
        
    def draw(self):
        self.root.mainloop()

def create_multiple_overlays(rectangles):
    overlays = []
    for rect in rectangles:
        overlay = ScreenOverlay(width=rect['width'], height=rect['height'], x=rect['x'], y=rect['y'])
        overlays.append(overlay)
    
    for overlay in overlays:
        overlay.draw()

# Usage
if __name__ == "__main__":
    rectangles = [
        {'width': 170, 'height': 56, 'x': 1920 - 200, 'y': 300},
    ]
    create_multiple_overlays(rectangles)
