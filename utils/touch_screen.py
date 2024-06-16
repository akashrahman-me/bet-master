import subprocess

def touch_screen(x, y):
    subprocess.run(['adb', 'shell', 'input', 'tap', str(x), str(y)])