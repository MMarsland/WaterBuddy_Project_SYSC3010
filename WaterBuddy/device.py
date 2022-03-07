#Imports 
import sys
import time

# Local Classes
from buzzer import Buzzer
from display import Display
from firebaseAPI import FirebaseAPI
from flowSystem import FlowSystem
from localDatabase import LocalDatabase
try:
    from senseHatSensors import SenseHatSensors
    from senseHatDisplay import SenseHatDisplay
except Exception:
    pass

# Simulator Classes
sys.path.append('Simulators')
from buzzerSim import BuzzerSim
from displaySim import DisplaySim
from flowSystemSim import FlowSystemSim
from senseHatDisplaySim import SenseHatDisplaySim


class WaterBuddy:
    def __init__(self):
        self.id = 1 # "Can we get this from the hardware?" From local database maybe! Randomly generated first time? Unique
        
        self.firebaseAPI = FirebaseAPI()

        # Simulated Aspects (When running on an RPi with senseHat you can pass in a real SenseHatDisplay())
        self.display = Display(BuzzerSim(), SenseHatDisplaySim())

    def main(self):
        print("Device Established...")
        self.display.displayMessage(0, "Device Established...")
        self.loop(1)
        
    def loop(self, delay):
        #print("Loop")

        # Push Message to Database
        #try:
        #    inputArr = input("Send a Message {dest,message}: ").split(",")
        #    self.firebaseAPI.sendMessage(self.id, inputArr[0], inputArr[1])
        #except Exception:
        #    print("Failed to parse input and send message")
        try:
            inputName = input("Register a station: ")
            self.firebaseAPI.registerStation(inputName)
        except Exception as e:
            print(f"Failed to register station: {e}")

        try:
            # Check Database for Messages directed at this senseHat
            messages = self.firebaseAPI.getMessages(self.id)
            print(messages)
            if messages:
                for message in messages:
                    print(message)
        except Exception:
            print("Failed to get and print messages")

        time.sleep(delay)
        self.loop(delay)

if __name__ == "__main__":
    try:
        water_buddy = WaterBuddy()
        water_buddy.main()
    except KeyboardInterrupt:
        print("Interrupeted")
    print("Exiting")