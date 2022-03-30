import sys
sys.path.append('../../../')
sys.path.append('../../../Simulators')
from buzzerSim import BuzzerSim
from senseHatDisplay import SenseHatDisplay

# Tests that require user input must be run with "pytest -s"

def test_init():
    buzzer = BuzzerSim(SenseHatDisplay())
    assert (not buzzer == None)

def test_playChimeLocal():
    buzzer = BuzzerSim(SenseHatDisplay())
    buzzer.playChime("local")
    assert (input('\nDid you see the text "Local Message: "? (y/n): ') == "y")

def test_playChimeStation():
    buzzer = BuzzerSim(SenseHatDisplay())
    buzzer.playChime("station")
    assert (input('\nDid you see the text "Station Message: "? (y/n): ') == "y")

def test_playChimeApplication():
    buzzer = BuzzerSim(SenseHatDisplay())
    buzzer.playChime("application")
    assert (input('\nDid you see the text "App Message: "? (y/n): ') == "y")
