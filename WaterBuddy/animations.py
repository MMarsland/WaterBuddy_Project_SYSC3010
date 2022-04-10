# -----------------------------------------------------------
# This file contains the code for supporting the animations
# that are displayed on the senseHat. These are built from
# the frames defined in the Animations class and these classes
# provide modularity to the animations framework.
#
# display.py controls the creation of animations.
#
#
# Written by Michael Marsland and Caleb Turcotte, April 2022
# -----------------------------------------------------------

import time
import threading
import math

class Animations():
    # Defining colours
    W = (0,0,255) # Water
    C = (255, 255, 255) # Cup
    B = (0,0,0) # Background
    F = (255, 128, 0) # Floor
    E = (255, 255, 0) # Emoji

    # Defining Frames
    cup_empty = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, C, C, C, B, B,
        F, F, F, F, F, F, F, F]

    cup_filling = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, C, C, C, B, B,
        F, F, F, F, F, F, F, F]

    cup_filling2 = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, C, C, C, B, B,
        F, F, F, F, F, F, F, F]

    cup_full = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, C, B, B, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, W, W, C, B, B,
        B, B, C, C, C, C, B, B,
        F, F, F, F, F, F, F, F]

    shout_emoji = [
        B, B, E, E, E, E, B, B,
        B, E, B, B, B, B, E, B,
        E, B, E, B, B, E, B, E,
        E, B, B, B, B, B, B, E,
        E, B, B, E, E, B, B, E,
        E, B, B, E, E, B, B, E,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B]

    resting_emoji = [
        B, B, E, E, E, E, B, B,
        B, E, B, B, B, B, E, B,
        E, B, E, B, B, E, B, E,
        E, B, B, B, B, B, B, E,
        E, B, B, B, B, B, B, E,
        E, B, E, E, E, E, B, E,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B]

    happy_emoji = [
        B, B, E, E, E, E, B, B,
        B, E, B, B, B, B, E, B,
        E, B, E, B, B, E, B, E,
        E, B, B, B, B, B, B, E,
        E, B, E, B, B, E, B, E,
        E, B, B, E, E, B, B, E,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B]

    sad_emoji = [
        B, B, E, E, E, E, B, B,
        B, E, B, B, B, B, E, B,
        E, B, E, B, B, E, B, E,
        E, B, B, B, B, B, B, E,
        E, B, B, E, E, B, B, E,
        E, B, E, B, B, E, B, E,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B]

    smile1 = [
        B, B, B, B, B, B, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, B, B, B, B, B, B,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    smile2 = [    
        B, B, B, B, B, B, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        E, B, E, B, B, E, B, E,
        E, B, B, B, B, B, B, E,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    blink1 = [
        B, B, B, B, B, B, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, B, B, B, B, B, B,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    blink2 = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    wink1 = [
        B, B, B, B, B, B, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, E, B, B, E, B, B,
        B, B, B, B, B, B, B, B,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    wink2 = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, E, B, B,
        B, E, E, E, B, E, B, B,
        B, B, B, B, B, E, B, B,
        B, B, B, B, B, B, B, B,
        B, E, B, B, B, B, E, B,
        B, B, E, E, E, E, B, B,
        B, B, B, B, B, B, B, B]

    blank = [
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B,
        B, B, B, B, B, B, B, B]


    def __init__(self, senseHat):
        self.senseHat = senseHat

    def getAnimation(self, animationName, durationFrames, interruptable):
        if (animationName == "filling"):
            return Animation(self.senseHat, [self.cup_empty, self.cup_filling, self.cup_filling2, self.cup_full], durationFrames, interruptable)
        elif (animationName == "smile"):
            return Animation(self.senseHat, [self.smile1, self.smile2], durationFrames, interruptable)
        elif (animationName == "blink"):
            return Animation(self.senseHat, [self.blink1, self.blink2], durationFrames, interruptable)
        elif (animationName == "wink"):
            return Animation(self.senseHat, [self.wink1, self.wink2], durationFrames, interruptable)

class Animation():
    def __init__(self, senseHat, frames, durationFrames, interruptable):
        self.senseHat = senseHat
        self.frames = frames
        self.durationFrames = durationFrames
        self.interruptable = interruptable
        self.pause = False
        self.stop = False
    
    def show(self):
        frameCount = 0
        while not self.stop and frameCount < self.durationFrames:
            if (not self.pause):
                self.senseHat.setPixels(self.frames[frameCount % len(self.frames)])
                time.sleep(0.6)
                frameCount = (frameCount + 1)
        self.senseHat.clear()
