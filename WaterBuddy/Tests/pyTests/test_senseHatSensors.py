# -----------------------------------------------------------
# pyTest unit tests for the SenseHatSensors class
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------


import sys
sys.path.append('../../')
sys.path.append('../../Simulators')
from senseHatSensors import SenseHatSensors

import warnings

def test_init():
    sensors = SenseHatSensors()
    assert not (sensors == None)
    return sensors

def test_getHumidity():
    sensors = SenseHatSensors()
    humidity = sensors.getHumidity()
    assert isinstance(humidity, float)
    # Check Decimal Places
    assert len(f"{humidity}".split(".")[1]) <= 2

    if humidity == 0:
        warnings.warn(UserWarning("Reading Humidity as (0.00)."))
