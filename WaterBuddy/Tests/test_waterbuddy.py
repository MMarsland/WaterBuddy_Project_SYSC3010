import sys
sys.path.append('../WaterBuddy/')
sys.path.append('../WaterBuddy/Simulators')
from waterbuddy import WaterBuddy

def test_init():
    print("Running Test init")
    wb = WaterBuddy(True, True)
    assert (not wb.firebaseAPI == None)