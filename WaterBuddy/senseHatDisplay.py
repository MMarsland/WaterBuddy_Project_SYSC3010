from sense_hat import SenseHat
from random import randint
import time
import threading


# For thread saftey, these display methods should only be called through the Display class
class SenseHatDisplay():
    def __init__(self):
        self.sense = SenseHat()

    def showMessage(self, message):
        color = self.getRandomColour()
        speed = 0.025
        self.sense.show_message(message, text_colour=color, scroll_speed=speed)

    def flashWord(self, word, delay):
        color = self.getRandomColour()
        for letter in word:
            self.sense.show_letter(letter, color)
            time.sleep(delay)
        self.sense.clear()

    def flash(self, color):
        self.sense.clear(color)
        time.sleep(0.5)
        self.sense.clear()

    def setPixels(self, pixels):
        self.sense.set_pixels(pixels)

    def getRandomColour(self):
         r = randint(100, 255)
         g = randint(100, 255)
         b = randint(100, 255)
         return (r, g, b)

    def clear(self):
        self.sense.clear()