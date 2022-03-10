import pyrebase
from dataStructures import StationData

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
    
    def updateDatabase(self, path, payload):
        dest = self.database
        for child in path.split("/"):
            dest = dest.child(child)
        dest.set(payload)

    def sendMessage(self, src, dest, message):
        self.database.child("messages").push({"dest": dest, "src": src, "message": message})

    def getMessages(self):
        messages = self.database.child("messages").order_by_child("dest").equal_to(self.stationID).get()
        
        objMessages = []
        for message in messages.each():
            objMessages.append(message.val())
            self.database.child("messages").child(message.key()).remove()
        return objMessages

    def stationRegistered(self):
        return (not self.database.child(f"stations/{self.stationID}").shallow().get().val() == None)

    def registerStation(self, stationData):
        self.updateDatabase(f"stations/{self.stationID}", { "cupSize": stationData.cupSize, 
                                                            "humidity": 0, 
                                                            "mute": stationData.mute, 
                                                            "waterFrequency": stationData.waterFrequency, 
                                                            "displayNotificationsFromFriends": stationData.displayNotificationsFromFriends})

    def getStationData(self):
        data = self.database.child("stations").child(self.stationID).get().val()
        return StationData(cupSize=data["cupSize"], mute=data["mute"], waterFrequency=data["waterFrequency"], displayNotificationsFromFriends=data["displayNotificationsFromFriends"])

    def updateHumidity(self, humidity):
        self.updateDatabase(f"stations/{self.stationID}/humidity", humidity)


