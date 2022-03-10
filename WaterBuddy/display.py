import sys
import time

# Import Simulators
sys.path.append('Simulators')


# Is this a good candidate for a module? Maybe, but only if sensehat and pizeo were also modules...
class Display():
    def __init__(self, senseHat, buzzer):
        self.senseHat = senseHat
        self.buzzer = buzzer
        pass

    def displayMessage(self, code, message):
        self.buzzer.playChime(code)
        time.sleep(2)
        self.senseHat.showMessage(message)


