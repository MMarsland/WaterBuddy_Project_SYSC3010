import sys
sys.path.append('../../../WaterBuddy/')
sys.path.append('../../../WaterBuddy/Simulators')
from buzzerSim import BuzzerSim

def test_init():
    buzzer = BuzzerSim()
    assert (not buzzer == None)

def test_playChimeLocal():
    buzzer = BuzzerSim()
    buzzer.playChime("local")

def test_playChimeStation():
    buzzer = BuzzerSim()
    buzzer.playChime("station")

def test_playChimeApplication():
    buzzer = BuzzerSim()
    buzzer.playChime("application")
    assert (input('Did you see: "BuzzerSim.playChime("application")" (y/n): ') == "y")
