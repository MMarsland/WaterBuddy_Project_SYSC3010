import time, sys
import RPi.GPIO as GPIO
sys.path.append('../../')
from fillSystem import CupSensor

cupSensor = CupSensor(17, 27) # Instantiate CupSensor object on BCM pins 17 & 27

while 1:
    try:
        distance = cupSensor.getDistance()
        if distance <= 3: # If an object is placed within 3cm of the sensor
            print("CUP DETECTED\n")

        time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting")
        GPIO.cleanup()
        sys.exit()
