import time, sys
import RPi.GPIO as GPIO
sys.path.append('../../')
from buzzer import Buzzer

buzzer = Buzzer(12) # Instantiate buzzer object on BCM pin 12 (PWM0)

print("Playing chime 0...")
buzzer.playChime(0)
time.sleep(1)

print("Playing chime 1...")
buzzer.playChime(1)
time.sleep(1)

print("Playing chime 2...")
buzzer.playChime(2)

GPIO.cleanup()
