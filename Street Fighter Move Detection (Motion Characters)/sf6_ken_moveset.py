from pynput import keyboard

inputHistory = []

class keyInput:
    def __init__(self, direction, frames):
        self.direction = direction
        self.frames = frames
    
    def direction (self):
        return self.direction
    
    def frames (self):
        return self.frames

def keyPressed (key):
    print(str(key))
