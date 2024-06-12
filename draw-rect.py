from lib.ScreenOverlay import create_multiple_overlays

rectangles = [
        {'width': 170, 'height': 56, 'x': 1920 - 200, 'y': 300},
        {'width': 420, 'height': 64, 'x': 1470, 'y': 645},
    ]
create_multiple_overlays(rectangles)