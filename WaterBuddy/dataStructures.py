# -----------------------------------------------------------
# The dataStructures file defines the various python dataclasses
# used throughout the program to control and unify data for the
# station, users, waterData, and messages.
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------


from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

@dataclass
class StationData:
    '''
    This data structure defines the stationData that is stored in the system
    and in the local database. This data structure only encompasses the parts
    of stationData required to run the station in offline mode.
    '''
    cupSize: float = 355
    displayNotificationsFromFriends: bool = False
    mute: bool = False

@dataclass
class UserData:
    '''
    This data structure defines the userData that is stored in the system
    and in the local database.
    '''
    userID: str = "John Doe"
    friends: list = field(default_factory=list)
    stations: list = field(default_factory=list)
    isAdmin: bool = False
    height: float = 0.0
    weight: float = 0.0
    thirst: int = 1

@dataclass
class WaterData:
    '''
    This data structure defines a WaterData which is an element of the
    water hisotry array both in the firebase and local databases.
    '''
    datetime: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount: float = 0.0

@dataclass
class Message:
    '''
    This data structure defines a message in the system. These are built when
    sending or receiving messages to/from the firebase database.
    '''
    source: str = ""
    dest: str = ""
    message: str = ""
    extras: dict = field(default_factory=dict)

    def isFriendNotification(self):
        return self.extras.get("friendNotification", False) == True