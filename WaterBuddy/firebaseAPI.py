import pyrebase

class FirebaseAPI():
    def __init__(self):
        self.config = {
            "apiKey": "AIzaSyD9u5VpKks9lUKqJ2W1SAZvbF1u6JgWh5k",
            "authDomain": "water-buddy-79d13.firebaseapp.com",
            "databaseURL": "https://water-buddy-79d13-default-rtdb.firebaseio.com/",
            "storageBucket": "water-buddy-79d13.appspot.com"
        }
        self.database = pyrebase.initialize_app(self.config).database()
        # "project_number": "571567331576",
        pass

    def sendMessage(self, src, dest, message):
        self.database.child("messages").push({"dest": dest, "src": src, "message": message})

    def getMessages(self, id):
        messages = self.database.child("messages").get() #.order_by_child("dest").equal_to(f"{id}").get()
        # Delete Messages
        #database.child("Michael-Test").child("messages").order_by_child("dest").equal_to(f"{id}").remove()
        objMessages = []
        for message in messages.each():
            key = message.key()
            #print(key)
            messageVal = message.val()
            #print(messageVal["dest"])
            if messageVal["dest"] == f"{id}":
                objMessages.append(messageVal)
                self.database.child("messages").child(f"{key}").remove()
        return objMessages

    def registerStation(self, stationID):
        self.updateDatabase(f"stations/{stationID}", {"cupSize": 25, "dailyWater": 0, "humidity": 25, "mute": False, "waterFrequency": 0, "weeklyWater": 0})

    def updateDatabase(self, path, payload):
        dest = self.database
        for child in path.split("/"):
            dest = dest.child(child)
        dest.set(payload)
