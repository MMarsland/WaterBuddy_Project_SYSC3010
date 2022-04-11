import time, sys
import RPi.GPIO as GPIO
sys.path.append('../')
from fillSystem import CupSensor
from fillSystem import Relay
from fillSystem import FlowSensor
from buzzer import Buzzer

# Instantiate hardware objects with GPIO pin numbers
cupSensor = CupSensor(17, 27)
relay = Relay(26)
flowSensor = FlowSensor(22)
buzzer = Buzzer(12)

# Infinite loop polls cup sensor, if cup is detected, turn relay on,
# play buzzer chime and poll flow sensor 3 times, then turn relay off
while 1:
    try:
        distance = cupSensor.getDistance()
        if distance <= 5:
            relay.on()
            for i in range(3):
                buzzer.playChime(0)
                flowSensor.getFlowRate()
            relay.off()
    except KeyboardInterrupt:
            print("Exiting")
            GPIO.cleanup()
            sys.exit()
