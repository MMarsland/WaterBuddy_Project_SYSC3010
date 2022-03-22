class BuzzerSim():
    def __init__(self, senseHatDisplay):
        self.senseHatDisplay = senseHatDisplay
    
    def playChime(self, code):
        if code == "local" or code == 0:
            # Locally Spawnned Notification
            pass
            
        elif code == "station" or code == 1:
                # Other Water Buddy Notification
                pass
        elif code == "application" or code == 2:
                # Other Application Notification
                pass
            # More cases for more chime options, drink reminders, entertainment chimes, etc...
        print(f'BuzzerSim.playChime("{code}")')
        self.senseHatDisplay.flash((255,0,0))
