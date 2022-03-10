#Imports 
import sys
import time
from datetime import datetime

# Local Classes
from dataStructures import StationData, UserData
from buzzer import Buzzer
from display import Display
from firebaseAPI import FirebaseAPI
from localDatabase import LocalDatabase
try:
    from senseHatSensors import SenseHatSensors
    from senseHatDisplay import SenseHatDisplay
    from fillSystem import FillSystem
except Exception:
    pass

# Simulator Classes
sys.path.append('Simulators')
from buzzerSim import BuzzerSim
from fillSystemSim import FillSystemSim
from senseHatDisplaySim import SenseHatDisplaySim
from senseHatSensorsSim import SenseHatSensorsSim

# Basic Hydration Amounts
#https://www.healthline.com/health/how-much-water-should-I-drink#recommendations
#https://www.nap.edu/read/10925/chapter/6#144
# children 4–8 years old	5 cups, or 40 oz. (1.18L)
# children 9–13 years old	7–8 cups, or 56–64 oz. (1.66-1.89)
# children 14–18 years old	8–11 cups, or 64–88 oz. (1.89-2.6)
# men 19 years and older	13 cups, or 104 oz. (3.07)  -> 160lbs
# women 19 years and older	9 cups, or 72 oz. (2.1)     -> 110lbs
# pregnant women	10 cups, or 80 oz. (2.36)
# breastfeeding women	13 cups, or 104 oz. (3.07)

# 15-30 ml per pound (0.5 to 1 oz)
# weight(lbs)x0.66(oz/lbs)x30(ml/oz)x0.001(L/mL) -> L

# Weight is the only factor it would seem (aside from breastfeeding)
# We may need to cut height since height and weight are already realated
# We could replace it with age? (https://www.weightwatchers.com/ca/en/article/how-much-water-should-you-drink-every-day)
# Activity level is a factor! (Add 12oz=355ml) per 30 minutes of exercise (https://www.slenderkitchen.com/article/how-to-calculate-how-much-water-you-should-drink-a-day)


class WaterBuddy:
    def __init__(self, stationID, simulateFillSystem, simulateRPi):
        self.stationID = stationID # "Can we get this from the hardware?" From local database maybe! Randomly generated first time? Unique
        
        self.firebaseAPI = FirebaseAPI(self.stationID)

        if (simulateRPi):
            # Simulated Aspects (When running on an RPi with senseHat you can pass in a real SenseHatDisplay())
            self.display = Display(SenseHatDisplaySim(), BuzzerSim())
            self.sensors = SenseHatSensorsSim()
        elif (simulateFillSystem):
            self.display = Display(SenseHatDisplay(), BuzzerSim())
            self.sensors = SenseHatSensors()
        else:
            self.display = Display(SenseHatDisplay(), Buzzer())
            self.sensors = SenseHatSensors()

        self.lastHumidiySendTime = None
        self.lastFillTime = None

        self.userData = UserData()
        self.stationData = StationData()

    def main(self):
        print("Welcome to Water Buddy!")
        self.display.displayMessage("local", "Welcome to Water Buddy!")

        print("Ensuring the station is registered")
        if (not self.firebaseAPI.stationRegistered()):
            print("Registering Station")
            self.firebaseAPI.registerStation(self.stationData)
        else:
            print("Station Already Registered")
        # Check for local database or create one

        # Get userdata from owner

        self.loop(1)
        
    def loop(self, delay):
        while (True):

            # Upload Himidity to Database every second
            if (not self.lastHumidiySendTime or time.time() - self.lastHumidiySendTime > 5):
                self.lastHumidiySendTime = time.time()
                # Get Humidity
                humidity = self.sensors.getHumidity()
                # Send Humidity
                self.firebaseAPI.updateHumidity(humidity)
                print(f"Humidity of {humidity} uploaded at {datetime.now().strftime('%H:%M:%S')}")

            # Check for updates to the database (UserData, StationData) and update local database
            stationData = self.firebaseAPI.getStationData()
            if (not self.stationData == stationData):
                # Station Data changed: recalcualte waterFrequency, update local database
                self.stationData = stationData
                print(self.stationData)

            # Check for updates in User data and update local datatbase (Perhaps we should set up streams for these)

            # Update station data (WaterFrequency) if userdata changed and send to firebase

            # Check Database for Messages directed at this senseHat
            messageObjs = self.firebaseAPI.getMessages()
            for messageObj in messageObjs:
                # Act on the message
                self.display.displayMessage(("station" if ("Station" in messageObj["source"]) else "application"), messageObj["message"])

            # Dispatch local "Drink water" notification if required

            # Poll the ultrasonic sensor (Fill System (Start fill system thread + block another thread from starting))
            # This will run the whole fill system process which results in updates to the local database, the local database module will handle passing the waterhistory to firebase.

            time.sleep(delay)

if __name__ == '__main__':
    try:
        water_buddy = WaterBuddy("Station 1", True, False)
        water_buddy.main()
    except KeyboardInterrupt:
        print("Interrupeted")
    print("Exiting")