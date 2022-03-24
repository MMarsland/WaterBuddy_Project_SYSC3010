from sense_hat import SenseHat
import random

class FillSystemSim():
    def __init__(self, senseHatDisplay):
        self.senseHatDisplay = senseHatDisplay
        self.cupSensor = CupSensorSim()

    def poll(self):
        
        # Ultrasonic sensor triggered, run fill system!

        # Simulate fill system

        # addWater History

        # NEED TO RESEARCH PASSING DATA FROM A THREAD so we can get water data/call a function...
        pass

class CupSensorSim():
    def __init__(self):
        self.sense = SenseHat()
    
    def getDistance(self):
        distance = 10.0000

        for event in self.sense.stick.get_events():
            if event.direction == "middle":
                distance = 2.0000
        #print("Distance: {:.3f} cm\n".format(distance))
        return distance

class RelaySim():
    def __init__(self):
        pass

    def on(self):
        print("RelaySim.on()")

    def off(self):
        print("RelaySim.off()")

class FlowSensorSim():
    def __init__(self):
        pass

    def detectEdge(self, channel):
        print("FlowSensorSim.detectEdge()")

    # Poll the sensor for 'interval' seconds and return the flow rate
    def getFlowRate(self, interval):

        flowRate = random.random()*10
        print("Flow rate: {:.3f} L/min\n".format(flowRate))
        return flowRate

if __name__ == "__main__":
    #fs = FillSystemSim()
    #while True:
        #fs.poll()
        #time.sleep(3)
    pass
