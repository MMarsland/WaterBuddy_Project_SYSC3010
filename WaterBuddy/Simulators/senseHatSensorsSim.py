from random import random

class SenseHatSensorsSim():
    def __init__(self):
        pass

    def getHumidity(self):
        print("SenseHatSensorsSim.getHumidity()")
        return round(random() * 5 + 20, 2)
