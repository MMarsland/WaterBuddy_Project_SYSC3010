# -----------------------------------------------------------
# This file contains the main code for The WaterBuddy project.
# This file creates and instance of the WaterBuddy class with
# the given stationID and a flag differentiating if the instantiated
# WaterBuddy is a simulator (WaterBuddy Minus) or a full system.
#
# The WaterBuddy class contains the main() function which is called
# to start the WaterBuddy system and the loop() function which runs
# the WaterBuddy's main loop as well as other helper functions for the
# WaterBuddy that didn't fit in any of the accompanying module classes
# utilized by the WaterBuddy Code. Further documentantion is included 
# in the code to describe the functionality of these methods.
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------


# Imports
import RPi.GPIO as GPIO 
import sys
import time
import random

# Local Classes
from dataStructures import StationData, UserData
from display import Display
from firebaseAPI import FirebaseAPI
from localDatabase import LocalDatabase
try:
    from senseHatSensors import SenseHatSensors
    from senseHatDisplay import SenseHatDisplay
    from fillSystem import FillSystem
    from buzzer import Buzzer
except Exception as e:
    print(e)

# Simulator Classes
sys.path.append('Simulators')
from buzzerSim import BuzzerSim
from fillSystemSim import FillSystemSim


class WaterBuddy:
    '''The main class for The WaterBuddy System.
    
    Each WaterBuddy or WaterBuddy Minus station must instantiate an
    instance of the WaterBuddy class and call it's main() function.
    '''

    def __init__(self, stationID, simulator=False):
        '''
        Instantiates the WaterBuddy class either as a simulator (For the
        WaterBuddy Minus) or as a full system with the attached fill
        system hardware. The provided stationID should be unique in the system
        '''

        self.stationID = stationID
        self.waterFrequency = 3600
        self.humidity = 0
        self.lastHumiditySendTime = time.time()
        self.lastFillOrNotificationTime = time.time()
        self.lastAnimationTime = time.time()

        self.firebaseAPI = FirebaseAPI(self.stationID)
        self.localDatabase = LocalDatabase()
        self.sensors = SenseHatSensors()

        if (simulator):
            self.display = Display(SenseHatDisplay(rotation=180), BuzzerSim(SenseHatDisplay()))
            self.fillSystem = FillSystemSim(self.display, self)
        else:
            self.display = Display(SenseHatDisplay(), Buzzer(12))
            self.fillSystem = FillSystem(self)

        self.userData = UserData()
        self.stationData = StationData()

        self.dataChanged = True

    def main(self):
        '''Starts the WaterBuddy running.

        Attempts to establish a connection to the Firebase database or
        local database and beings running the WaterBuddy loop.
        '''

        self.display.displayMessage("Welcome to WaterBuddy!", "local")
        self.display.startAnimation("smile", durationFrames=6)

        self.online = True
        try:
            self.firebaseAPI.ensureStationRegistered(self.stationData)

            self.userData = self.firebaseAPI.getUserDataFromStationID()
            self.stationData = self.firebaseAPI.getStationData()

        except ConnectionError as e:
            # Unable to establish a connection to the firebase database
            self.online = False
            self.display.displayMessage("No Internet Connection...", "local")

            # Try to get user and station data from local database instead
            self.stationData = self.localDatabase.getStationData()
            self.userData = self.localDatabase.getUserData()

            # If there is no distinct user data in the local database or firebaseAPI we cannot run the station.
            if (self.userData.userID == "John Doe"):
                self.display.displayMessage("This station must be registered to a user to run. Try registering this station through the application or connecting the station to the internet", "local")
                time.sleep(60)
                self.main()
                return
            
        self.loop(1)
        
    def loop(self, delay):
        '''The main code loop for the WaterBuddy station.

        This loop is run indefinitely while the WaterBuddy station is running.
        The loop contains several steps:
        1. Get messages from firebase directed at this station
        2. Check for changes to this stations data in firebase
        3. Check for changes to this station's user data in the firebase
        4. If stationData or userData has changed, update the local database
        and the waterFrequency of the station.
        5. Upload the station's humidity to the firebase database
        6. Run a check to see if the station has come online and can make
        a connection to the firebase database and if so, upload all water
        history stored in the local database.
        7. Poll the ultrasonic sensor to see if a fill should be run
        8. Check if a fill was just completed by the fill system thread
        9. Notify the user if the correct amount of time has passed since
        the last notification or fill
        10. Dispaly a random animation on the senseHat if the correct amount
        of time has passed since the last animation
        '''
        while (True):
            try:
                loopTime = time.time()
                if (self.online):
                    # Check Database for Messages directed at this senseHat
                    messages = self.firebaseAPI.getMessages()
                    for message in messages:
                        # Act on the message
                        if not self.stationData.mute and (not message.isFriendNotification() or self.stationData.displayNotificationsFromFriends):
                            self.display.displayMessage(message.message, ("station" if ("Station" in message.source) else "application"))

                    self.dataChanged = False
                    # Check for updates to the database (UserData, StationData) and update local database
                    stationData = self.firebaseAPI.getStationData()
                    if (not self.stationData == stationData):
                        # Station Data changed: recalcualte waterFrequency, update local database
                        self.stationData = stationData
                        self.dataChanged = True

                    # Check for updates in User data and update local datatbase & Recalculate Water Frequency (Perhaps we should set up streams for these)
                    userData = self.firebaseAPI.getUserData(self.userData.userID)
                    if (not self.userData == userData):
                        # Station Data changed: recalcualte waterFrequency, update local database
                        self.userData = userData
                        self.localDatabase.updateUserData(self.userData)
                        self.dataChanged = True
                    
                    if self.dataChanged:
                        self.updateWaterFrequency()
                        # Update station data (WaterFrequency) & Send to firebase (Or local Database...)
                        self.localDatabase.updateStationData(self.stationData)
                        self.firebaseAPI.updateWaterFrequency(self.waterFrequency)

                    # Upload Humidity to Database every delay
                    if (loopTime - self.lastHumiditySendTime > 5):
                        self.lastHumiditySendTime = loopTime
                        # Get Humidity
                        self.humidity = self.sensors.getHumidity()
                        # Send Humidity
                        self.firebaseAPI.updateHumidity(self.humidity)
                        #print(f"Humidity of {humidity} uploaded at {datetime.now().strftime('%H:%M:%S')}")
                        self.updateWaterFrequency()
                        self.firebaseAPI.updateWaterFrequency(self.waterFrequency)

                # Check if we have come online
                if not self.online:
                    try:
                        self.firebaseAPI.ensureStationRegistered(self.stationData)
                        self.online = True
                        # Now that we are online, Dispatch local "Drink water" notification if required
                        self.uploadWaterHistory()

                    except ConnectionError:
                        self.online = False

                # Poll the ultrasonic sensor (Fill System (Start fill system thread + block another thread from starting))
                if not self.fillSystem.filling:
                    if (self.fillSystem.poll()):
                        self.display.startAnimation("filling")
                else:
                    self.lastAnimationTime = loopTime
                    self.lastFillOrNotificationTime = loopTime

                if self.fillSystem.waterData:
                    self.addWaterHistory(self.fillSystem.waterData)
                    self.notifyFriends(self.fillSystem.waterData)
                    self.fillSystem.waterData = None
                    self.display.stopAnimation()
                    self.display.startAnimation("smile", durationFrames=6)

                # Notify the user if it's time to drink water!
                if (loopTime - self.lastFillOrNotificationTime > self.waterFrequency):
                    self.lastFillOrNotificationTime = loopTime
                    if not self.stationData.mute:
                        self.display.displayMessage("It's time for a glass of water!", "local")
                        self.display.startAnimation("smile", durationFrames=6)

                    # Notify on the app that it's time for water!
                    self.firebaseAPI.sendMessage(dest=self.userData.userID, 
                                                 message=f"It's time for another glass of water!")

                if (not self.stationData.mute and (loopTime - self.lastAnimationTime > 30)):
                    self.lastAnimationTime = loopTime
                    animationNum = random.randint(0,1)
                    if (animationNum == 0):
                        self.display.startAnimation("blink", durationFrames=7)
                    elif (animationNum == 1):
                        self.display.startAnimation("wink", durationFrames=7)

            except ConnectionError:
                self.online = False

            time.sleep(delay)

    def updateWaterFrequency(self):
        # -----------------------------------------------------------
        # Basic Hydration Amounts
        # https://www.healthline.com/health/how-much-water-should-I-drink#recommendations
        # https://www.nap.edu/read/10925/chapter/6#144
        # children 4–8 years old	5 cups, or 40 oz. (1.18L)
        # children 9–13 years old	7–8 cups, or 56–64 oz. (1.66-1.89)
        # children 14–18 years old	8–11 cups, or 64–88 oz. (1.89-2.6)
        # men 19 years and older	13 cups, or 104 oz. (3.07)  -> 160lbs
        # women 19 years and older	9 cups, or 72 oz. (2.1)     -> 110lbs
        # pregnant women	10 cups, or 80 oz. (2.36)
        # breastfeeding women	13 cups, or 104 oz. (3.07)

        # 15-30 ml per pound (0.5 to 1 oz)
        # weight(lbs)x0.66(oz/lbs)x30(ml/oz)x0.001(L/mL) -> L

        # Weight is the only factor it would seem (aside from breastfeeding)
        # We may need to cut height since height and weight are already realated
        # We could replace it with age? (https://www.weightwatchers.com/ca/en/article/how-much-water-should-you-drink-every-day)
        # Activity level is a factor! (Add 12oz=355ml) per 30 minutes of exercise (https://www.slenderkitchen.com/article/how-to-calculate-how-much-water-you-should-drink-a-day)

        # "Thirst" accounts for activity level
        # Parched, Thirsty, Average, Hydrophobic (355ml per each level)

        # Hours at desk 8 or number of waking hours 16
        # Amount of water Per day = f(weight, thirst)
        # Number of cups = f(cupSize, Amount of water Per day)
        # cupsPerHour = f(numberOfCups, hours)
        # Water frequency = f(cupsPerHour)
        # Very this based on humidity (0=dry , 100=wet)
        # -----------------------------------------------------------

        workDayHours = 8 # For now we will give the user all their required water within their work day
        waterFrequency = 3600
        try:
            mLPerDay = (self.userData.weight*2.2) * 2/3 * 29.5735/1 + 355 * (self.userData.thirst-1) # kg * oz/kg * ml/oz = ml
            numOfCups = mLPerDay / self.stationData.cupSize # ml/day / ml/cup = cups/day
            cupsPerHour = numOfCups / workDayHours # cups/day / hours/day = cups/hour
            waterFrequency = 3600 / cupsPerHour # 1 / cups/hour * sec/hour = secs/cup
            waterFrequency = waterFrequency * ((100 + self.humidity/10)/100) # Time between cups increases as humidity increases
        except Exception as e:
            print(e)
            pass

        self.waterFrequency = waterFrequency
        
    def addWaterHistory(self, waterData):
        if (self.online):
            try:
                # Upload to Firebase
                self.firebaseAPI.addWaterHistory(waterData)
                return
            except ConnectionError:
                self.online = False
        if (not self.online):
            # Local Database
            self.localDatabase.addWaterHistory(waterData)
        
    def uploadWaterHistory(self):
        # Upload all water history rows to firebase and then delete the 
        # entries from the local database (Would be issues (Double uploads) if we upload some 
        # and then go offline... Could fix this by going row by row and deleting as we go)
        # We could thread this but then need to be careful of going offline while in a thread
        waterHistory = self.localDatabase.getWaterHistory()

        for waterData in waterHistory:
            self.firebaseAPI.addWaterHistory(waterData)

        self.localDatabase.deleteWaterHistory()

    def notifyFriends(self, waterData):
        # For each friend, send a message to each of their statons station
        for friendID in self.userData.friends:
            friendData = self.firebaseAPI.getUserData(friendID)
            for stationID in friendData.stations:
                self.firebaseAPI.sendMessage(dest=stationID, 
                                             message=f"{self.userData.userID} has just finished a glass of water!",
                                             extras={"friendNotification": True})

            # For each friend, also send a message to their application
            self.firebaseAPI.sendMessage(dest=friendID, 
                                         message=f"Your friend {self.userData.userID} has just finished a glass of water! Get drinking!",
                                         extras={"friendNotification": True})


# The main code for the WaterBuddy system instantiates either a simulator
# (WaterBuddy Minus) or a full station with the give stationID and calls
# its main loop to start the station running.
if __name__ == '__main__':
    try:
        water_buddy = WaterBuddy(stationID="Station 70", simulator=True)
        water_buddy.main()
        
    except KeyboardInterrupt:
        print("Interrupted")
        GPIO.cleanup()
    print("Exiting")