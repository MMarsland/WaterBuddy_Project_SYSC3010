#Imports 
import sys
import time

# Local Classes
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


class WaterBuddy:
    def __init__(self, simulateFillSystem, simulateRPi):
        self.id = 1 # "Can we get this from the hardware?" From local database maybe! Randomly generated first time? Unique
        
        self.firebaseAPI = FirebaseAPI(self.id)

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

        self.lastHumidiySendTime = time.time()

    def main(self):
        print("Device Established...")
        self.display.displayMessage(0, "Device Established...")
        print("Ensuring the station is registered")
        if (not self.firebaseAPI.stationRegistered()):
            print("Registering Station")
            self.firebaseAPI.registerStation()
        else:
            print("Station Already Registered")


        self.loop(1)
        
    def loop(self, delay):
        #print("Loop")

        # Upload Himidity to Database every second
        if (time.time() - self.lastHumidiySendTime > 1):
            self.lastHumidiySendTime = time.time()
            # Get Humidity
            humidity = self.sensors.getHumidity()
            # Send Humidity
            self.firebaseAPI.updateHumidity(humidity)

        # Push Message to Database
        #try:
        #    inputArr = input("Send a Message {dest,message}: ").split(",")
        #    self.firebaseAPI.sendMessage(self.id, inputArr[0], inputArr[1])
        #except Exception:
        #    print("Failed to parse input and send message")
        #try:
        #    inputName = input("Register a station: ")
        #    self.firebaseAPI.registerStation()
        #except Exception as e:
        #    print(f"Failed to register station: {e}")


        # Check Database for Messages directed at this senseHat
        try:
            messages = self.firebaseAPI.getMessages(self.id)
            #print(messages)
            if messages:
                for message in messages:
                    # Act on the message
                    print(message)
        except Exception:
            print("Failed to get and print messages")

        time.sleep(delay)
        self.loop(delay)

if __name__ == '__main__':
    try:
        water_buddy = WaterBuddy(True, True)
        water_buddy.main()
    except KeyboardInterrupt:
        print("Interrupeted")
    print("Exiting")