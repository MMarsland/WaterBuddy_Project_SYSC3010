# -----------------------------------------------------------
# The SenseHatSensors class acts as a module for getting data from
# the senseHat's humidity sensor.
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------

from sense_hat import SenseHat


class SenseHatSensors():
    def __init__(self):
        self.sense = SenseHat()

    def getHumidity(self):
        return round(self.sense.get_humidity(), 2)