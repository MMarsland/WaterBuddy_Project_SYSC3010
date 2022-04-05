import RPi.GPIO as GPIO
import time
import threading
from dataStructures import WaterData

class FillSystem():
    def __init__(self, waterBuddy):
        self.waterBuddy = waterBuddy
        self.cupSensor = CupSensor(17, 27)
        self.relay = Relay(26)
        self.flowSensor = FlowSensor(22)

        self.cupFillMargin = 50  # How many mL to fill short of the cupSize
        self.flowSensorInterval = 0.1  # Flow sensor poll interval in seconds

        self.waterData = None
        self.filling = False

    # Poll the cup sensor, if cup is detected,
    # start the fill system thread
    def poll(self):
        if (self.cupSensor.triggered()):
            self.filling = True
            # Display Filling Animation 
            fillThread = threading.Thread(target=self.fillSystemThread)
            fillThread.start()
            return True
        return False

    # Thread function
    def fillSystemThread(self):
        self.relay.on()  # Turn on water pump

        # Loop polling Flow Sensor (Recording amount flowed)
        amount = 0
        while amount < ((self.waterBuddy.stationData.cupSize
                        - self.cupFillMargin) * 0.75):
            amount = amount + (self.flowSensor.getFlowRate(
                               self.flowSensorInterval)
                               * self.flowSensorInterval)

        self.relay.off()  # Turn off water pump

        # When the whole process is done return
        # a new waterdata with the amount filled
        self.waterData = WaterData(amount=amount)

        distance = 0
        while distance < 10:
            distance = self.cupSensor.getDistance()
            time.sleep(1)

        time.sleep(10)

        self.filling = False


class CupSensor():
    def __init__(self, trigger, echo):
        self.TRIGGER_PIN = trigger
        self.ECHO_PIN = echo

        # Setup GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIGGER_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Measure distance to nearest object
    def getDistance(self):
        # Send a 10us pulse to the TRIGGER
        GPIO.output(self.TRIGGER_PIN, 1)
        time.sleep(0.00001)
        GPIO.output(self.TRIGGER_PIN, 0)

        startTime = time.time()
        stopTime = time.time()

        # Wait for ECHO to be driven high by the sensor
        while GPIO.input(self.ECHO_PIN) == 0:
            startTime = time.time()

        # Wait for ECHO to be driven low by the sensor
        while GPIO.input(self.ECHO_PIN) == 1:
            stopTime = time.time()

        elapsed = stopTime - startTime

        # Distance = time * speed of sound (in cm/s)
        distance = (elapsed * 34300) / 2
        print("Distance: {:.3f} cm\n".format(distance))
        return distance

    # Return true if sensor distance is < 3cm
    def triggered(self):
        return self.getDistance() < 4


class Relay():
    def __init__(self, pin):
        self.RELAY_PIN = pin

        # Setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)

    # Turn the relay on
    def on(self):
        GPIO.output(self.RELAY_PIN, 1)

    # Turn the relay off
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

        # Sensor is active LOW, use internal pull-up resistor
        GPIO.setup(self.SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Setup interrupts
        GPIO.add_event_detect(self.SENSOR_PIN, GPIO.FALLING,
                              callback=self.detectEdge)

    # This function is meant to be used as the ISR for the sensor pin
    # (i.e. it fires everytime a falling edge is detected)
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

        # Frequency to flow rate conversion from sensor datasheet
        flowRate = ((_edgeCount / interval) / 11)*(1000/60)
        print("Flow rate: {:.3f} mL/sec\n".format(flowRate))
        return flowRate
