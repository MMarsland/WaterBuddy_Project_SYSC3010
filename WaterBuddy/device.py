import time
import threading

senseHat = False
try:
    from helper_functions import sensehat
    senseHat = True
except:
    pass
from helper_functions import database

class WaterBuddy:
    def __init__(self):
        self.id = 10 #"Can we get this from the hardware?"
        self.input = None
        self.input_thread = threading.Thread(target=user_input, args=(self,))

    def main(self):
        print("Device Established...")
        if senseHat: sensehat.displayMessage("Device Established...")
        self.loop(0.1)
        

    def loop(self, delay):
        #print("Loop")

        # Check Database for Messages directed at this senseHat
        messages = database.getMessages(self.id)
        #print(messages)
        if messages:
            for message in messages:
                print(message)

        if self.input:
            #print(self.input)
            # Send Message
            data = self.input.split(",")
            database.sendMessage(data[0], data[1], data[2])

        if not self.input_thread.is_alive():
            self.input_thread = threading.Thread(target=user_input, args=(self,))
            self.input_thread.start()

        time.sleep(delay)
        self.loop(delay)

def user_input(device):
    device.input = None
    device.input = input("Send Message 'id,msg': ")
    

if __name__ == "__main__":
    water_buddy = WaterBuddy()
    water_buddy.main()