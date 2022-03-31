import sys
import time
import threading
import math
        
from animations import Animations

class Display():
    def __init__(self, senseHat, buzzer):
        self.senseHat = senseHat
        self.buzzer = buzzer
        self.animations = Animations(senseHat)

        self.animation = None
        
        self.animationThread = None
        self.displayThread = None

    def displayMessage(self, message, buzzerCode="none"):
        def displayMessageThread(self, lastDisplayThread, message, buzzerCode):   
            if not self.animationThread is None:
                self.animationThread.join()
            if not lastDisplayThread is None:
                lastDisplayThread.join()

            self.buzzer.playChime(buzzerCode)
            #time.sleep(2)
            self.senseHat.showMessage(message)

        
        # Made a thread for this process
        self.displayThread = threading.Thread(target=displayMessageThread, args=(self, self.displayThread, message, buzzerCode))
        self.displayThread.start()

    def flash(self, color):
        def flashThread(self, lastDisplayThread, color):
            if not self.animationThread is None:
                self.animationThread.join()
            if not lastDisplayThread is None:
                lastDisplayThread.join()

            self.senseHat.flash(color)

        # Made a thread for this process
        self.displayThread = threading.Thread(target=flashThread, args=(self, self.displayThread, color))
        self.displayThread.start()

    def startAnimation(self, animationName, durationFrames=math.inf, interruptable=False):
        self.stopAnimation()

        def animationThread(self, lastAnimationThread, animationName, durationFrames, interruptable):
            if not lastAnimationThread is None:
                lastAnimationThread.join()
            if not self.displayThread is None:
                self.displayThread.join()

            self.animation = self.animations.getAnimation(animationName, durationFrames, interruptable)
            self.animation.start()

        self.animationThread = threading.Thread(target=animationThread, args=(self, self.animationThread, animationName, durationFrames, interruptable))
        self.animationThread.start()

    def pauseAnimation(self):
        if not self.animation is None:
            self.animation.pause = True

    def resumeAnimation(self):
        if not self.animation is None:
            self.animation.pasue = False

    def stopAnimation(self):
        if not self.animation is None:
            self.animation.stop = True
        self.animation = None
        


