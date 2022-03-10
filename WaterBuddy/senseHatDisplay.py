from sense_hat import SenseHat
from random import randint
import time

class SenseHatDisplay():
    def __init__(self):
        self.sense = SenseHat()
        pass

    def showMessage(self, message):
        color = self.getRandomColour()
        speed = 0.05
        self.sense.show_message(message, text_colour=color, scroll_speed=speed)

    def flashWord(self, word, delay):
        color = self.getRandomColour()
        for letter in word:
            self.sense.show_letter(letter, color)
            time.sleep(delay)

    def getRandomColour(self,):
         r = randint(50, 255)
         g = randint(50, 255)
         b = randint(50, 255)
         return (r, g, b)