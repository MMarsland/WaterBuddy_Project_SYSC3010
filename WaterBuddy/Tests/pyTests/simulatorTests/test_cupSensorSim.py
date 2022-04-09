# -----------------------------------------------------------
# pyTest unit tests for the cupSensorSim class
#
# These unit tests ensure the senseHat Joystick press is detected properly.
#
# Written by Michael Marsland, April 2022
# -----------------------------------------------------------

import sys, time
sys.path.append('../../../')
sys.path.append('../../../Simulators')
from fillSystemSim import CupSensorSim

def test_init():
    cupSensor = CupSensorSim()
    assert(not cupSensor == None)

def test_CupSensor():
    cupSensor = CupSensorSim()
    detected = True
    print("\nPolling for joystick press..")
    count = 10
    while count > 0:
        print(count)
        count = count - 1
        distance = cupSensor.getDistance()
        if distance <= 3:
            detected = True
            break
        else:
            detected = False
        time.sleep(1)

    assert(detected == True)
