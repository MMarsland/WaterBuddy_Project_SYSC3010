import time
import threading

senseHatAvaliable = True
from senseHatAPI import SenseHatAPI
from senseHatAPISim import SenseHatAPISim
import localDatabase
from firebaseAPI import FirebaseAPI

class WaterBuddy:
    def __init__(self):
        self.id = 1 # "Can we get this from the hardware?" From local database maybe! Randomly generated first time? Unique
        
        self.firebaseAPI = FirebaseAPI()

        # Simulated Aspects
        self.senseHatAPI = SenseHatAPISim()

    def main(self):
        print("Device Established...")
        self.senseHatAPI.displayMessage("Device Established...")
        self.loop(0.1)
        
    def loop(self, delay):
        #print("Loop")

        # Push Message to Database
        try:
            inputArr = input("Send a Message {dest,message}: ").split(",")
            self.firebaseAPI.sendMessage(self.id, inputArr[0], inputArr[1])
        except Exception:
            print("Failed to parse input and send message")

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