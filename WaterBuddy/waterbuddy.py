#Imports 
import sys
import time
from datetime import datetime

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


# Process for connection to new customer's internet?
class WaterBuddy:
    def __init__(self, stationID, simulator=False):
        self.stationID = stationID # "Can we get this from the hardware?" From local database maybe! Randomly generated first time? Unique
        self.waterFrequency = 3600
        self.lastHumidiySendTime = None
        self.lastFillTime = None

        self.firebaseAPI = FirebaseAPI(self.stationID)
        self.localDatabase = LocalDatabase()
        self.sensors = SenseHatSensors()

        if (simulator):
            self.display = Display(SenseHatDisplay(), BuzzerSim(SenseHatDisplay()))
            self.fillSystem = FillSystemSim(SenseHatDisplay())
        else:
            self.display = Display(SenseHatDisplay(), Buzzer())
            self.fillSystem = FillSystem(self)

        self.userData = UserData()
        self.stationData = StationData()

    def main(self):
        print("Welcome to WaterBuddy!")
        self.display.displayMessage("local", "Welcome to WaterBuddy!")

        self.online = True
        try:
            print("Ensuring the station is registered")
            if (not self.firebaseAPI.isStationRegistered()):
                print("Registering Station")
                self.firebaseAPI.registerStation(self.stationData)
            else:
                print("Station Already Registered")
        except ConnectionError as e:
            self.online = False
            self.display.displayMessage("local", "No Internet Connection...")

        # Try to get user and station data from local database
        self.stationData = self.localDatabase.getStationData()
        self.userData = self.localDatabase.getUserData()

        # Calculate inital water frequency
        self.updateWaterFrequency()

        try:
            # Get userdata from owner (From Either Firebase or LocalDatabase)
            if (self.userData.userID == "John Doe"):
                # We don't have any user data stored in localDatabase
                # Find Owner from firebase
                self.userData = self.firebaseAPI.getUserDataFromStationID()
                self.localDatabase.updateUserData(self.userData)
                self.dataChanged = True
        
        except ConnectionError as e:
            print("This station must be registered to a user to run, try registering this station through the application or connecting the station to the internet")
            self.display.displayMessage("local", "This station must be registered to a user to run, try registering this station through the application or connecting the station to the internet")
            time.sleep(10)
            self.main()

        

        self.loop(1)
        
    def loop(self, delay):
        while (True):
            try:
                if (self.online):
                    # Check Database for Messages directed at this senseHat
                    messageObjs = self.firebaseAPI.getMessages()
                    for messageObj in messageObjs:
                        # Act on the message
                        self.display.displayMessage(("station" if ("Station" in messageObj["source"]) else "application"), messageObj["message"])

                    dataChanged = False
                    # Check for updates to the database (UserData, StationData) and update local database
                    stationData = self.firebaseAPI.getStationData()
                    if (not self.stationData == stationData):
                        # Station Data changed: recalcualte waterFrequency, update local database
                        self.stationData = stationData
                        dataChanged = True

                    # Check for updates in User data and update local datatbase & Recalculate Water Frequency (Perhaps we should set up streams for these)
                    userData = self.firebaseAPI.getUserData(self.userData.userID)
                    if (not self.userData == userData):
                        # Station Data changed: recalcualte waterFrequency, update local database
                        self.userData = userData
                        self.localDatabase.updateUserData(self.userData)
                        dataChanged = True
                    
                    if dataChanged:
                        self.updateWaterFrequency()
                        # Update station data (WaterFrequency) & Send to firebase (Or local Database...)
                        self.localDatabase.updateStationData(self.stationData)
                        self.firebaseAPI.updateWaterFrequency(self.waterFrequency)

                    # Upload Humidity to Database every delay
                    if (not self.lastHumidiySendTime or (time.time() - self.lastHumidiySendTime > 5)):
                        self.lastHumidiySendTime = time.time()
                        # Get Humidity
                        humidity = self.sensors.getHumidity()
                        # Send Humidity
                        self.firebaseAPI.updateHumidity(humidity)
                        #print(f"Humidity of {humidity} uploaded at {datetime.now().strftime('%H:%M:%S')}")

                # Check if we have come online
                try:
                    self.firebaseAPI.ensureStationRegistered(self.stationData)
                    self.online = True
                    # Now that we are online, Dispatch local "Drink water" notification if required
                    self.uploadWaterHistory()

                except ConnectionError:
                    self.online = False

                # Poll the ultrasonic sensor (Fill System (Start fill system thread + block another thread from starting))
                # This will run the whole fill system process which results in updates the water history (see "WaterBuddy.addWaterHistory") (Should also potentially notify friends)
                if not self.fillSystem.filling:
                    self.fillSystem.poll()
                # Maybe check if fillSystem thread is complete? Need to pass data from the thread? Can a thread make a callback on this thread?

                if self.fillSystem.waterData:
                    self.addWaterHistory(self.fillSystem.waterData)
                    self.fillSystem.waterData = None

            except ConnectionError:
                self.online = False

            time.sleep(delay)

    def updateWaterFrequency(self):
        # Recalucaltes the water frequency based on new StationData and/or new UserData

        # Basic Hydration Amounts
        #https://www.healthline.com/health/how-much-water-should-I-drink#recommendations
        #https://www.nap.edu/read/10925/chapter/6#144
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

        # Thirst can account for activity level
        # Parched, Thirsty, Average, Hydrophobic (add 355ml per each level)

        # Hours at desk 8 or number of waking hours 16
        # Amount of water Per day = f(weight, thirst)
        # Number of cups = f(cupSize)
        # cupsPerHour = f(numberOfCups, hours)
        # Water frequency = f(cupsPerHour)

        self.waterFrequency = 3600 # Defaults at 1 per hour
        
    def addWaterHistory(self, waterData):
        if (self.online):
            try:
                # Uplaod to Firebase
                self.firebaseAPI.addWaterHistory(waterData)
                # Notify Friends
                return
            except ConnectionError:
                self.online = False
        if (not self.online):
            # Local Database
            self.localDatabase.addWaterHistory(waterData)
        
    def uploadWaterHistory(self):
        # Upload all water history rows to firebase and then delete the enteries from the local database (Would be issues (Double uploads) if we upload some and then go offline... Could fix this by going row by row and deleting as we go)
        # We could thread this but then need to be careful of going offline while in a thread
        #self.lastDisplayMessageThread = threading.Thread(target=displayMessageThread, args=(self, code, message, self.lastDisplayMessageThread))
        #self.lastDisplayMessageThread.start()
        waterHistory = self.localDatabase.getWaterHistory()

        for waterData in waterHistory:
            self.firebaseAPI.addWaterHistory(waterData)

        self.localDatabase.deleteWaterHistory()




if __name__ == '__main__':
    try:
        water_buddy = WaterBuddy("Station 1", True)
        water_buddy.main()
    except KeyboardInterrupt:
        print("Interrupeted")
    print("Exiting")