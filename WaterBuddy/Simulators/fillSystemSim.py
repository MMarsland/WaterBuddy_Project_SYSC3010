# -----------------------------------------------------------
# The FillSystemSim class duck type implements the same functionality
# as the FillSystem class in fillSystem.py allowing the other waterbuddy
# code to use either the real fill system or this simulator interchangeably.
#
# Unlike the real fill system this simulated class doesn't require a relay
# or fill system and instead just assumes the user refills their cup to their
# set cupSize. The senseHat joystick is used to simulate the triggering of the
# Ultrasonic cup sensor.
#
# Written by Michael Marsland and Nick Milani, April 2022
# -----------------------------------------------------------

from sense_hat import SenseHat
import threading
import time
import sys
sys.path.append('../')
from dataStructures import WaterData


class FillSystemSim():
    def __init__(self, display, waterBuddy):
        self.waterBuddy = waterBuddy
        self.display = display
        self.cupSensor = CupSensorSim()

        self.filling = False
        self.waterData = None
        
    def poll(self):
        # if Joystick Pressed, run fill simulated system!
        if self.cupSensor.triggered():
            self.display.displayMessage("Congratualtions! Go refill your cup!")
            # Start a new thread for the fill system, simulate fill system
            x = threading.Thread(target=self.fillSystemThread, args=(self.waterBuddy.stationData.cupSize,))
            x.start()
            return True
        return False

    def fillSystemThread(self, amount):
        self.filling = True
        
        time.sleep(10)

        self.waterData = WaterData(amount=amount)

        self.display.displayMessage("Keep on drinking!")

        while (self.cupSensor.getDistance() < 5):
            pass

        time.sleep(5)
        self.filling = False
        

class CupSensorSim():
    def __init__(self):
        self.sense = SenseHat()
    
    def getDistance(self):
        distance = 10.0000
        
        for event in self.sense.stick.get_events():
            if event.direction == "middle":
                distance = 2.0000
        return distance

    def triggered(self):
        return self.getDistance() < 3