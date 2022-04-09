# -----------------------------------------------------------
# The BuzzerSim class duck type implements the same functionality
# as the Buzzer class in buzzer.py allowing the other waterbuddy
# code to use either the real buzzer or this simulator interchangeably.
#
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------

class BuzzerSim():
    def __init__(self, senseHatDisplay):
        self.senseHatDisplay = senseHatDisplay
    
    def playChime(self, code):
        # Don't simulate any buzzer functionality
        # on "WaterBuddy Minus" just have this function
        # here to implement the buzzer interface
        return
