import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from waterbuddy import WaterBuddy

def test_init():
    #print("Running Test init")
    wb = WaterBuddy(True, True)
    assert (not wb == None)