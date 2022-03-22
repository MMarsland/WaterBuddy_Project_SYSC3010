import RPi.GPIO as GPIO
import time

class FillSystem():
    def __init__(self):
        pass

    def poll():
        pass

class CupSensor():
    def __init__(self, trigger, echo):
        self.TRIGGER_PIN = trigger
        self.ECHO_PIN = echo

        # Setup GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def getDistance(self):
        # Send a 10us pulse to the TRIGGER
        GPIO.output(self.TRIGGER_PIN, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER_PIN, 0)

        startTime = time.time()
        stopTime = time.time()

        while GPIO.input(self.ECHO_PIN) == 0: # Wait for ECHO to be driven high by the sensor
            startTime = time.time()

        while GPIO.input(self.ECHO_PIN) == 1: # Wait for ECHO to be driven low by the sensor
            stopTime = time.time()

        elapsed = stopTime - startTime
        distance = (elapsed * 34300) / 2 # Distance = time * speed of sound (in cm/s)
        print("Distance: {:.3f} cm\n".format(distance))
        return distance

class Relay():
    def __init__(self, pin):
        self.RELAY_PIN = pin

        # Setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)

    def on(self):
        GPIO.output(self.RELAY_PIN, 1)

    def off(self):
        GPIO.output(self.RELAY_PIN, 0)

class FlowSensor():

    global _edgeCount, _enable
    _edgeCount = 0
    _enable = 0

    def __init__(self, pin):
        self.SENSOR_PIN = pin

        # Setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Sensor is active LOW, use internal pull-up resistor
        GPIO.add_event_detect(self.SENSOR_PIN, GPIO.FALLING, callback=self.detectEdge) # Setup interrupts

    # This function is meant to be used as the ISR for the sensor pin (i.e. it fires everytime a falling edge is detected)
    def detectEdge(self, channel):
        global _edgeCount
        if _enable == 1:
            _edgeCount = _edgeCount + 1

    # Poll the sensor for 'interval' seconds and return the flow rate
    def getFlowRate(self, interval):
        global _edgeCount, _enable
        _edgeCount = 0
        _enable = 1
        time.sleep(interval)
        _enable = 0

        flowRate = ((_edgeCount / interval) / 11) # Frequency to flow rate conversion from sensor datasheet
        print("Flow rate: {:.3f} L/min\n".format(flowRate))
        return flowRate
