import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from waterbuddy import WaterBuddy

def test_init():
    #print("Running Test init")
    wb = WaterBuddy("Station 1", True)
    assert (not wb == None)