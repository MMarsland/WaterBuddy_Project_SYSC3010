# -----------------------------------------------------------
# pyTest unit tests for the FirebaseAPI class
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------


import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from firebaseAPI import FirebaseAPI

import time
from dataStructures import StationData
from dataStructures import UserData
from dataStructures import WaterData

def test_init():
    fb = FirebaseAPI("Station 99")
    assert not (fb == None)
    assert not (fb.database == None)

def test_updateDatabase():
    fb = FirebaseAPI("Station 99")
    
    fb.updateDatabase("tests/updateDatabase", {"working": True})

    fb.updateDatabase("tests", {})

def test_getFromDatabase():
    fb = FirebaseAPI("Station 99")
    
    fb.updateDatabase("tests/updateDatabase", {"working": True})

    working = fb.getFromDatabase("tests/updateDatabase/working")
    assert working == True
    fb.updateDatabase("tests", {})

def test_sendMessage_and_getMessages():
    fb = FirebaseAPI("Station 99")

    fb.sendMessage("Station 99", "Test Message!")

    messages = fb.getMessages()

    assert len(messages) == 1
    assert messages[0].source == "Station 99"
    assert messages[0].dest == "Station 99"
    assert messages[0].message == "Test Message!"

def test_isStationRegistered():
    fb = FirebaseAPI("Station 99")

    fb.updateDatabase("stations/Station 99", {})

    assert fb.isStationRegistered() == False

def test_registerStation():
    fb = FirebaseAPI("Station 99")
    stationData = StationData("Station 99")

    fb.registerStation(stationData)
    assert fb.isStationRegistered() == True

def test_ensureStationRegistered():
    fb = FirebaseAPI("Station 99")

    stationData = StationData("Station 99")

    fb.ensureStationRegistered(stationData)
    assert fb.isStationRegistered() == True 

def test_getStationData():
    fb = FirebaseAPI("Station 99")
    stationData = StationData("Station 99")

    fb.ensureStationRegistered(stationData)

    returnedStationData = fb.getStationData()
    assert returnedStationData == stationData

def test_updateHumidity():
    fb = FirebaseAPI("Station 99")
    humidity = 64.20
    fb.updateHumidity(humidity)

    returnedHumidity = fb.getFromDatabase("stations/Station 99/humidity")
    assert returnedHumidity == humidity

def test_updateWaterFrequency():
    fb = FirebaseAPI("Station 99")
    waterFrequency = 3200
    fb.updateWaterFrequency(waterFrequency)

    returnedWaterFrequency = fb.getFromDatabase("stations/Station 99/waterFrequency")
    assert returnedWaterFrequency == waterFrequency

def test_addWaterHistory():
    fb = FirebaseAPI("Station 99")
    waterData = WaterData(amount=480)
    
    fb.addWaterHistory(waterData)

    waterHistory = fb.getFromDatabase("stations/Station 99/waterHistory")
    assert len(list(waterHistory.items())) == 1
    assert list(waterHistory.items())[0][1]["amount"] == 480

def test_getUserData():
    fb = fb = FirebaseAPI("Station 99")

    fb.updateDatabase("users/testUser", {"userID": "testUser", "stations": ["Station 99"]})

    returnedUserData = fb.getUserData("testUser")
    assert returnedUserData.userID == "testUser"
    fb.updateDatabase("users/testUser", {})

def test_getUserDataFromStationID():
    fb = fb = FirebaseAPI("Station 99")
    fb.updateDatabase("users/testUser", {"userID": "testUser", "stations": ["Station 99"]})

    returnedUserData = fb.getUserDataFromStationID()
    assert returnedUserData.userID == "testUser"
    fb.updateDatabase("users/testUser", {})
    
def test_clean_up():
    fb = FirebaseAPI("Station 99")
    fb.updateDatabase("stations/Station 99", {})
    fb.updateDatabase("users/testUser", {})
    fb.updateDatabase("tests", {})