import time, sys
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
            sys.exit()
