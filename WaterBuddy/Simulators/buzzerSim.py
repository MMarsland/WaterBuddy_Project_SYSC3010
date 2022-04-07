class BuzzerSim():
    def __init__(self, senseHatDisplay):
        self.senseHatDisplay = senseHatDisplay
    
    def playChime(self, code):
        # Don't simulate any buzzer funcationality
        # on "WaterBuddy Minus"
        return


        if code == "local" or code == 0:
            # Locally Spawnned Notification
            self.senseHatDisplay.showMessage("Local Mesage: ")
        elif code == "station" or code == 1:
            # Other Water Buddy Notification
            self.senseHatDisplay.showMessage("Station Mesage: ")
        elif code == "application" or code == 2:
            # Other Application Notification
            self.senseHatDisplay.showMessage("App Mesage: ")
        
