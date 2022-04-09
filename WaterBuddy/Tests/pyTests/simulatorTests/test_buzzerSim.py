# -----------------------------------------------------------
# pyTest unit tests for the buzzerSim class
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------

import sys
sys.path.append('../../../')
sys.path.append('../../../Simulators')
from buzzerSim import BuzzerSim
from senseHatDisplay import SenseHatDisplay

def test_init():
    buzzer = BuzzerSim(SenseHatDisplay())
    assert (not buzzer == None)

def test_playChime():
    buzzer = BuzzerSim(SenseHatDisplay())
    buzzer.playChime()
