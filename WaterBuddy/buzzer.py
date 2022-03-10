import RPi.GPIO as GPIO
import time

class Buzzer():

    dc = 70 # Duty cycle for the PWM pin

    def __init__(self, pin):
        self.BUZZER_PIN = pin

        # Setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)

    def playChime(self, code):
        if code == "local" or code == 0:
            # Locally Spawnned Notification
            pwm = GPIO.PWM(self.BUZZER_PIN, 1000) # Initial frequency: 1kHz
            pwm.start(self.dc)
            time.sleep(0.5)
            pwm.ChangeFrequency(2000)
            time.sleep(0.5)
            pwm.ChangeFrequency(3000)
            time.sleep(0.5)
            pwm.stop
        elif code == "station" or code == 1:
                # Other Water Buddy Notification
                pass
        elif code == "application" or code == 2:
                # Other Application Notification
                pass
            # More cases for more chime options, drink reminders, entertainment chimes, etc...
