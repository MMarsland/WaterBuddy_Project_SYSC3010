import time, sys
import RPi.GPIO as GPIO
sys.path.append('../../')
from fillSystem import Relay

relay = Relay(26) # Instantiate relay object on BCM pin 26

print("Turning relay on...")
time.sleep(1) # Give one second after heads-up message
relay.on()

time.sleep(3) # Keep relay on for 3 seconds
print("Turning relay off...")
relay.off()

GPIO.cleanup()
