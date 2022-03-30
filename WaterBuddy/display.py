import sys
import time
import threading
        
# Import Simulators
sys.path.append('Simulators')


class Display():
    def __init__(self, senseHat, buzzer):
        self.senseHat = senseHat
        self.buzzer = buzzer

        self.lastDisplayThread = None

    def displayMessage(self, message, buzzerCode="none"):
        def displayMessageThread(self, lastThread, message, buzzerCode):
            if not lastThread == None:
                lastThread.join()

            self.buzzer.playChime(buzzerCode)
            #time.sleep(2)
            self.senseHat.showMessage(message)

        # Made a thread for this process
        self.lastDisplayThread = threading.Thread(target=displayMessageThread, args=(self, self.lastDisplayThread, message, buzzerCode))
        self.lastDisplayThread.start()

    def flash(self, color):
        def flashThread(self, lastThread, color):
            if not lastThread == None:
                lastThread.join()

            self.senseHat.flash(color)

        # Made a thread for this process
        self.lastDisplayThread = threading.Thread(target=flashThread, args=(self, self.lastDisplayThread, color))
        self.lastDisplayThread.start()
        


