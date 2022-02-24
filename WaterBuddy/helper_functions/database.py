import pyrebase

config = {
    "apiKey": "AIzaSyANwedPY8RvO5lgs2zaskMONvDazk358V4",
    "authDomain": "sysc3010-f6daa.firebaseapp.com",
    "databaseURL": "https://sysc3010-f6daa-default-rtdb.firebaseio.com/",
    "storageBucket": "sysc3010-f6daa.appspot.com"
}

database = pyrebase.initialize_app(config).database()

def getMessages(id):
    messages = database.child("Project").child("messages").get()#.order_by_child("dest").equal_to(f"{id}").get()
    # Delete Messages
    #database.child("Project").child("messages").order_by_child("dest").equal_to(f"{id}").remove()
    objMessages = []
    for message in messages.each():
        key = message.key()
        #print(key)
        messageVal = message.val()
        #print(message["dest"])
        if messageVal["dest"] == f"{id}":
            objMessages.append(messageVal)
            database.child("Project").child("messages").child(f"{key}").remove()
   
    return objMessages

def sendMessage(dest, src, message):
    database.child("Project").child("messages").push({"dest": dest, "src": src, "message": message})
