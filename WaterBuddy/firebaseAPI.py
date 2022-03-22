import pyrebase
from dataStructures import StationData
from dataStructures import UserData
from dataStructures import WaterData

class FirebaseAPI():
    def __init__(self, stationID):
        self.config = {
            "apiKey": "AIzaSyD9u5VpKks9lUKqJ2W1SAZvbF1u6JgWh5k",
            "authDomain": "water-buddy-79d13.firebaseapp.com",
            "databaseURL": "https://water-buddy-79d13-default-rtdb.firebaseio.com/",
            "storageBucket": "water-buddy-79d13.appspot.com"
        }
        self.database = pyrebase.initialize_app(self.config).database()
        
        self.stationID = stationID
    
    # --- Generic Database Update ---
    def updateDatabase(self, path, payload):
        dest = self.database
        for child in path.split("/"):
            dest = dest.child(child)
        dest.set(payload)

    # --- Message Passing ---
    def sendMessage(self, src, dest, message):
        self.database.child("messages").push({"dest": dest, "src": src, "message": message})

    def getMessages(self):
        messages = self.database.child("messages").order_by_child("dest").equal_to(self.stationID).get()
        
        objMessages = []
        for message in messages.each():
            objMessages.append(message.val())
            self.database.child("messages").child(message.key()).remove()
        return objMessages

    
    # --- Data Retrival ---
    def getStationData(self):
        data = self.database.child("stations").child(self.stationID).get().val()
        return StationData(cupSize=data["cupSize"], mute=data["mute"], displayNotificationsFromFriends=data["displayNotificationsFromFriends"])

    def getUserData(self, userID):
        data = self.database.child("users").child(userID).get().val()
        return UserData(userID=data["userID"], friends=data.get("friends", []), stations=data.get("stations", []), isAdmin=data["isAdmin"], height=data["height"], weight=data["weight"], thirst=data["thirst"])

    def getUserDataFromStationID(self):
        userID = ""
        # Find the (first) user that owns this station
        # For the scope of the project this works (If large list of users this would likely break the program...)
        users = self.database.child("users").order_by_key().get()
        for user in users.each():
            
            userData = user.val()
            #print(userData)
            #print(hasattr(userData, "height"))
            #print(getattr(userData, "isAdmin", [0]))
            if (self.stationID in userData.get('stations', [])): # {name": "Mortimer 'Morty' Smith"}
                # User owning this station found
                userID = userData["userID"]
                break

        # If no users own this station, throw a connection error
        if (userID == ""):
            raise ConnectionError()

        # Pull their data
        # Return a userData object with their data
        return self.getUserData(userID)

    # --- Updating Station Data ---
    def updateHumidity(self, humidity):
        self.updateDatabase(f"stations/{self.stationID}/humidity", humidity)

    def updateWaterFrequency(self, waterFrequency):
        self.updateDatabase(f"stations/{self.stationID}/waterFrequency", waterFrequency)

    # Adding Water History
    def addWaterHistory(self, waterData):
        # Add a water history entry to the database
        self.database.child(f"stations/{self.stationID}/waterHistory").push({"datetime": waterData.datetime, "amount": waterData.amount})

    # --- Station Registering ---
    def isStationRegistered(self):
        return (not self.database.child(f"stations/{self.stationID}").shallow().get().val() == None)

    def registerStation(self, stationData):
        self.updateDatabase(f"stations/{self.stationID}", { "stationID": self.stationID,
                                                            "cupSize": stationData.cupSize, 
                                                            "humidity": 0, 
                                                            "mute": stationData.mute, 
                                                            "waterFrequency": 3600, 
                                                            "displayNotificationsFromFriends": stationData.displayNotificationsFromFriends})

    def ensureStationRegistered(self, stationData):
        if (not self.firebaseAPI.isStationRegistered()):
            self.firebaseAPI.registerStation(self.stationData)
