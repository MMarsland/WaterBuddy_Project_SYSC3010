from dataclasses import dataclass

@dataclass
class StationData:
    cupSize: float = 355
    mute: bool = False
    waterFrequency: float = 3600
    displayNotificationsFromFriends: bool = False

@dataclass
class UserData:
    id: str = "John Doe"
    height: float = 0.0
    weight: float = 0.0
    thirst: str = "less"