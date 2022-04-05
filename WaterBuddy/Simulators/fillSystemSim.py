from sense_hat import SenseHat
import threading
import time
import sys
sys.path.append('../')
from dataStructures import WaterData


class FillSystemSim():
    def __init__(self, display, waterBuddy):
        self.waterBuddy = waterBuddy
        self.display = display
        self.cupSensor = CupSensorSim()

        self.filling = False
        self.waterData = None
        
    def poll(self):
        # Ultrasonic sensor triggered, run fill system!
        if self.cupSensor.triggered():
            self.display.displayMessage("Congratualtions! Go refill your cup!")
            # Start a new thread for the fill system, simulate fill system\
            #print("Starting Fill Thread")
            x = threading.Thread(target=self.fillSystemThread, args=(self.waterBuddy.stationData.cupSize,))
            x.start()
            return True
        return False

    def fillSystemThread(self, amount):
        self.filling = True
        
        time.sleep(10)

        self.waterData = WaterData(amount=amount)

        self.display.displayMessage("Keep on drinking!")

        while (self.cupSensor.getDistance() < 5):
            pass

        time.sleep(5)
        self.filling = False
        


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

    def triggered(self):
        return self.getDistance() < 3



# class RelaySim():
#     def __init__(self):
#         pass

#     def on(self):
#         print("RelaySim.on()")

#     def off(self):
#         print("RelaySim.off()")

# class FlowSensorSim():
#     def __init__(self):
#         pass

#     def detectEdge(self, channel):
#         print("FlowSensorSim.detectEdge()")

#     # Poll the sensor for 'interval' seconds and return the flow rate
#     def getFlowRate(self, interval):

#         flowRate = random.random()*10
#         print("Flow rate: {:.3f} L/min\n".format(flowRate))
#         return flowRate

if __name__ == "__main__":
    #fs = FillSystemSim()
    #while True:
        #fs.poll()
        #time.sleep(3)
    pass
