import sys
import time
import threading
        
# Import Simulators
sys.path.append('Simulators')


class Display():
    def __init__(self, senseHat, buzzer):
        self.senseHat = senseHat
        self.buzzer = buzzer

        self.lastDisplayMessageThread = None


    def displayMessage(self, code, message):
        def displayMessageThread(self, code, message, lastThread):
            if not lastThread == None:
                lastThread.join()

            self.buzzer.playChime(code)
            #time.sleep(2)
            self.senseHat.showMessage(message)

        # Made a thread for this process
        self.lastDisplayMessageThread = threading.Thread(target=displayMessageThread, args=(self, code, message, self.lastDisplayMessageThread))
        self.lastDisplayMessageThread.start()
        


