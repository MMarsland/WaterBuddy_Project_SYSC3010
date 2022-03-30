import pyrebase
from dataStructures import StationData, UserData, Message


class FirebaseAPI():
    def __init__(self, stationID):
        self.stationID = stationID

        self.config = {
            "apiKey": "AIzaSyD9u5VpKks9lUKqJ2W1SAZvbF1u6JgWh5k",
            "authDomain": "water-buddy-79d13.firebaseapp.com",
            "databaseURL": "https://water-buddy-79d13-default-rtdb.firebaseio.com/",
            "storageBucket": "water-buddy-79d13.appspot.com"
        }
        self.database = pyrebase.initialize_app(self.config).database()

    # --- Generic Database Update ---
    def updateDatabase(self, path, payload):
        dest = self.database
        for child in path.split("/"):
            dest = dest.child(child)
        dest.set(payload)

    def getFromDatabase(self, path):
        src = self.database
        for child in path.split("/"):
            src = src.child(child)
        return src.get().val()

    # --- Message Passing ---
    def sendMessage(self, dest, message, extras={}):
        message = {"source": self.stationID, "dest": dest, "message": message, "extras": {}}
        for key, extra in extras.items():
            message.get("extras")[key] = extra
        self.database.child("messages").push(message)

    def getMessages(self):
        rawMessages = self.database.child("messages")\
                       .order_by_child("dest")\
                       .equal_to(self.stationID).get()

        messages = []
        for rawMessage in rawMessages.each():
            messageValue = rawMessage.val()
            
            messages.append(Message(source=messageValue.get("source"), 
                                    dest=messageValue.get("dest"), 
                                    message=messageValue.get("message"),
                                    extras=messageValue.get("extras", {})))

            self.database.child("messages").child(rawMessage.key()).remove()
        return messages

    # --- Data Retrival ---
    def getStationData(self):
        stationData = self.database.child("stations").child(self.stationID).get().val()
        return StationData(cupSize=stationData.get("cupSize"),
                           mute=stationData.get("mute"),
                           displayNotificationsFromFriends=stationData.get("displayNotificationsFromFriends"))

    def getUserData(self, userID):
        userData = self.database.child("users").child(userID).get().val()
        return UserData(userID=userData.get("userID"),
                        friends=userData.get("friends", []),
                        stations=userData.get("stations", []),
                        isAdmin=userData.get("isAdmin"),
                        height=userData.get("height"),
                        weight=userData.get("weight"),
                        thirst=userData.get("thirst"))

    def getUserDataFromStationID(self):
        userID = ""
        # Pulling all users works for the scope of the project
        # but would need to be refined for production scale
        users = self.database.child("users").order_by_key().get()
        for user in users.each():
            userData = user.val()
            if (self.stationID in userData.get('stations', [])):
                userID = userData.get("userID")
                break

        if (userID == ""):
            raise ConnectionError()

        return self.getUserData(userID)

    def getFriendsStations(self):

        pass

    # --- Updating Station Data ---
    def updateHumidity(self, humidity):
        self.updateDatabase(f"stations/{self.stationID}/humidity",
                            humidity)

    def updateWaterFrequency(self, waterFrequency):
        self.updateDatabase(f"stations/{self.stationID}/waterFrequency",
                            waterFrequency)

    def addWaterHistory(self, waterData):
        self.database.child(f"stations/{self.stationID}/waterHistory").push(
                            {"datetime": waterData.datetime,
                             "amount": waterData.amount})

    # --- Station Registering ---
    def isStationRegistered(self):
        return (not self.database.child(f"stations/{self.stationID}").shallow().get().val() is None)

    def registerStation(self, stationData):
        self.updateDatabase(f"stations/{self.stationID}",
                            {"stationID": self.stationID,
                             "cupSize": stationData.cupSize,
                             "humidity": 0,
                             "mute": stationData.mute,
                             "waterFrequency": 3600,
                             "displayNotificationsFromFriends": stationData.displayNotificationsFromFriends})

    def ensureStationRegistered(self, stationData):
        if (not self.isStationRegistered()):
            print("Registering Station")
            self.registerStation(stationData)
