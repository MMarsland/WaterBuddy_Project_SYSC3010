import time
import threading
import math

# Defining colours
W = (0,0,255) # Water
C = (255, 255, 255) # Cup
B = (0,0,0) # Background
F = (255, 128, 0) # Floor
E = (255, 255, 0) # Emoji

cup_empty = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, C, C, C, B, B,
    F, F, F, F, F, F, F, F
]

cup_filling = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, C, C, C, B, B,
    F, F, F, F, F, F, F, F
]

cup_filling2 = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, C, C, C, B, B,
    F, F, F, F, F, F, F, F
]

cup_full = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, C, B, B, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, W, W, C, B, B,
    B, B, C, C, C, C, B, B,
    F, F, F, F, F, F, F, F
]

shout_emoji = [
    B, B, E, E, E, E, B, B,
    B, E, B, B, B, B, E, B,
    E, B, E, B, B, E, B, E,
    E, B, B, B, B, B, B, E,
    E, B, B, E, E, B, B, E,
    E, B, B, E, E, B, B, E,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B
]

resting_emoji = [
    B, B, E, E, E, E, B, B,
    B, E, B, B, B, B, E, B,
    E, B, E, B, B, E, B, E,
    E, B, B, B, B, B, B, E,
    E, B, B, B, B, B, B, E,
    E, B, E, E, E, E, B, E,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B
]

happy_emoji = [
    B, B, E, E, E, E, B, B,
    B, E, B, B, B, B, E, B,
    E, B, E, B, B, E, B, E,
    E, B, B, B, B, B, B, E,
    E, B, E, B, B, E, B, E,
    E, B, B, E, E, B, B, E,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B
]

sad_emoji = [
    B, B, E, E, E, E, B, B,
    B, E, B, B, B, B, E, B,
    E, B, E, B, B, E, B, E,
    E, B, B, B, B, B, B, E,
    E, B, B, E, E, B, B, E,
    E, B, E, B, B, E, B, E,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B
]

smile1 = [
    B, B, B, B, B, B, B, B,
    B, B, E, B, B, E, B, B,
    B, B, E, B, B, E, B, B,
    B, B, E, B, B, E, B, B,
    B, B, B, B, B, B, B, B,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B,
    B, B, B, B, B, B, B, B
]

smile2 = [    
    B, B, B, B, B, B, B, B,
    B, B, E, B, B, E, B, B,
    B, B, E, B, B, E, B, B,
    E, B, E, B, B, E, B, E,
    E, B, B, B, B, B, B, E,
    B, E, B, B, B, B, E, B,
    B, B, E, E, E, E, B, B,
    B, B, B, B, B, B, B, B
]

blank = [
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B,
    B, B, B, B, B, B, B, B
]

class Animations():
    def __init__(self, senseHat):
        self.senseHat = senseHat

    def getAnimation(self, animationName, durationFrames, interruptable):
        if (animationName == "filling"):
            return Animation(self.senseHat, [cup_empty, cup_filling, cup_filling2, cup_full], durationFrames, interruptable)
        elif (animationName == "smile"):
            return Animation(self.senseHat, [smile1, smile2], durationFrames, interruptable)

class Animation():
    def __init__(self, senseHat, frames, durationFrames, interruptable):
        self.senseHat = senseHat
        self.frames = frames
        self.durationFrames = durationFrames
        self.interruptable = interruptable
        self.pause = False
        self.stop = False
    
    def start(self):
        frameCount = 0
        while not self.stop and frameCount < self.durationFrames:
            if (not self.pause):
                self.senseHat.setPixels(self.frames[frameCount % len(self.frames)])
                time.sleep(0.6)
                frameCount = (frameCount + 1)
        self.senseHat.clear()

        