# -----------------------------------------------------------
# pyTest unit tests for the LocalDatabase class
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------


import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from localDatabase import LocalDatabase

import os
import sqlite3

from dataStructures import UserData
from dataStructures import StationData
from dataStructures import WaterData

def test_init():
    testDatabasePath = "local_database.db"
    if os.path.exists(testDatabasePath):
        os.remove(testDatabasePath)

    db = LocalDatabase()
    assert (isinstance(db, LocalDatabase))

    # Ensure Tables Exist
    connection = sqlite3.connect('local_database.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='userData';")
    assert len(cursor.fetchall()) == 1

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='stationData';")
    assert len(cursor.fetchall()) == 1

    # Ensure userData and stationData tables have row to be updated
    cursor.execute("select COUNT (*) FROM userData;")
    rowCount = cursor.fetchall()[0][0]
    assert rowCount == 1

    cursor.execute("select COUNT (*) FROM stationData;")
    rowCount = cursor.fetchall()[0][0]
    assert rowCount == 1

    connection.commit()
    connection.close()
    
def test_updateUserData_and_getUserData():
    db = LocalDatabase()
    ud = UserData(userID="Larry Bird")

    db.updateUserData(ud)

    data = db.getUserData()

    assert (data.userID == "Larry Bird")

def test_updateStationData_and_getStationData():
    db = LocalDatabase()
    sd = StationData(cupSize=500)

    db.updateStationData(sd)

    data = db.getStationData()

    assert (data.cupSize == 500)

def test_addWaterHistory_and_getWaterHistory():
    db = LocalDatabase()
    wh = WaterData(amount = 480)

    db.addWaterHistory(wh)

    data = db.getWaterHistory()[-1]

    assert (data.amount == 480)

# Relies on previous test passing (Add and get)
def test_deleteWaterHistory():
    db = LocalDatabase()
    wh = WaterData(amount = 480)
    db.addWaterHistory(wh)

    wh = WaterData(amount = 480)
    db.addWaterHistory(wh)

    db.deleteWaterHistory()

    assert len(db.getWaterHistory()) == 0
        
def test_cleanUp():
    testDatabasePath = "local_database.db"
    if os.path.exists(testDatabasePath):
        os.remove(testDatabasePath)