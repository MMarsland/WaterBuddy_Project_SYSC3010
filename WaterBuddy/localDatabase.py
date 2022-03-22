import sqlite3
from dataStructures import StationData
from dataStructures import UserData
from dataStructures import WaterData

class LocalDatabase():
    def __init__(self):
        self.connection = sqlite3.connect('local_database.db') 
        self.connection.row_factory = sqlite3.Row
        self.db = self.connection.cursor()

        self.db.execute('''
                CREATE TABLE IF NOT EXISTS userData
                (userID TINYTEXT, height NUMERIC, weight NUMERIC, thirst TINYTEXT)
                ''')
                
        self.db.execute('''
                CREATE TABLE IF NOT EXISTS stationData
                (mute INTEGER, cupSize NUMERIC)
                ''')

        self.db.execute('''
                CREATE TABLE IF NOT EXISTS waterHistory
                (datetime DATETIME, amount NUMERIC)
                ''')
                            
        self.connection.commit()

        self.db.execute("select COUNT (*) FROM userData;")
        rowCount = self.db.fetchall()[0][0]
        if rowCount == 0:
            userData = UserData()
            self.db.execute("insert into userData values (?, ?, ?, ?);", (userData.userID, userData.height, userData.weight, userData.thirst))
            self.connection.commit()
        
        self.db.execute("select COUNT (*) FROM stationData;")
        rowCount = self.db.fetchall()[0][0]
        if rowCount == 0:
            stationData = StationData()
            self.db.execute("insert into stationData values (?, ?);", (stationData.mute, stationData.cupSize))
            self.connection.commit()


        
        # Other Maybe Helpful commands from LAB 2
        # cursor.execute("insert into weatherdata values (?, ?, ?, ?, ?, ?);", (city, datetime.now(), current["temp"], current["humidity"], current["pressure"], wind["speed"]))
        # df = pd.read_sql_query("SELECT * FROM sensordata;", dbconnect)[['temperature', 'humidity', 'pressure']]
        # df['pressure'] = df['pressure'].apply(lambda x: x/1000*30)
        # df.rename(columns={'temperature': 'Temperature', 'humidity': 'Humidity ', 'pressure': 'Pressure/1000*30'}, inplace=True)


    def updateUserData(self, userData):
        # Update the columns of userData with new userData
        self.db.execute("UPDATE userData SET userID = ?, height = ?, weight = ?, thirst = ?", (userData.userID, userData.height, userData.weight, userData.thirst))
        self.connection.commit()

    def updateStationData(self, stationData):
        #Update the columns of stationData with new stationData
        self.db.execute("UPDATE stationData SET mute = ?, cupSize = ?", (stationData.mute, stationData.cupSize))
        self.connection.commit()

    def addWaterHistory(self, waterData):
        # Add a water history row to the table
        self.db.execute("insert into waterHistory values (?, ?);", (waterData.datetime, waterData.amount))
        self.connection.commit()

    def getWaterHistory(self):
        self.db.execute("SELECT * from waterHistory;")
        rows = self.db.fetchall()
        waterHistory = []
        for row in rows:
            waterHistory.append(WaterHistory(datetime=row[0], amount=row[1]))
        return waterHistory

    def deleteWaterHistory(self):
        self.db.execute("DELETE from waterHistory;")
        self.connection.commit()

    def getStationData(self):
        # Retreve the stationData from the database
        self.db.execute("SELECT * from stationData;")
        data = self.db.fetchone()
        # Create and fill a stationData Object
        stationData = StationData(mute=data[0], cupSize=data[1])
        # Return the Station Data Object
        return stationData
        

    def getUserData(self):
        # Retreve the userData from the database
        self.db.execute("SELECT * from userData;")
        data = self.db.fetchone()
        # Create and fill a stationData Object
        userData = UserData(userID=data[0], height=data[1], weight=data[2], thirst=data[3])
        # Return the Station Data Object
        return userData

if __name__ == "__main__":
    #ld = LocalDatabase()
    #ld.updateUserData(UserData(userID="Larry Bird", weight=50))
    #print(ld.getUserData())
    pass

