from dataclasses import dataclass
from dataclasses import field
from datetime import datetime

@dataclass
class StationData:
    cupSize: float = 355
    displayNotificationsFromFriends: bool = False
    mute: bool = False

    def updateFrom(self, data):
        pass

@dataclass
class UserData:
    userID: str = "John Doe"
    friends: list = field(default_factory=list)
    stations: list = field(default_factory=list)
    isAdmin: bool = False
    height: float = 0.0
    weight: float = 0.0
    thirst: int = 1

    def updateFrom(self, data):
        pass

@dataclass
class WaterData:
    datetime: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount: float = 0.0

@dataclass
class Message:
    source: str = ""
    dest: str = ""
    message: str = ""
    extras: dict = field(default_factory=dict)

    def isFriendNotification(self):
        return self.extras.get("friendNotification", False) == True