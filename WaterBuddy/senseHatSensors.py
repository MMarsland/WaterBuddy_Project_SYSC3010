from sense_hat import SenseHat


class SenseHatSensors():
    def __init__(self):
        self.sense = SenseHat()

    def getHumidity(self):
        return round(self.sense.get_humidity(), 2)