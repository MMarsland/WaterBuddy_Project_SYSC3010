import time, sys
import RPi.GPIO as GPIO
sys.path.append('../../')
from fillSystem import FlowSensor

flowSensor = FlowSensor(22) # Instantiate flowSensor object on BCM pin 22

while 1:
    try:
        flowRate = flowSensor.getFlowRate(1) # This function polls the flow sensor for 1 second, returns the avg flow rate during that second
        if flowRate != 0:
            print("WATER FLOW DETECTED\nFlow Rate: {:.f} L/min".format(flowRate))
    except KeyboardInterrupt:
        print("Exiting")
        GPIO.cleanup()
        sys.exit()
