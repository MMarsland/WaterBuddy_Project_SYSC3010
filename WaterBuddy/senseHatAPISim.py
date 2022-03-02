import time, math


class SenseHatAPISim():
    def __init__(self):
        pass

    def displayMessage(self, message):
        print(message)



# def get_sensehat():
#     return SenseHat()

# def alarm(sense, flash_time):
#     for second in range(0, math.ceil(flash_time/2)):
#         sense.clear((255,0,0))
#         time.sleep(1)
#         sense.clear()
#         time.sleep(1)

# def getRandColour():
#     r = randint(0, 255)
#     g = randint(0, 255)
#     b = randint(0, 255)
#     return (r, g, b)

# def flashWord(word, delay):
#     for letter in word:
#         sense.show_letter(letter, getRandColour())
#         sleep(delay)

# def displayValue(valueStruct):
#     flashWord(valueStruct[0], 0.2)
#     sense.show_message("{:.2f}".format(valueStruct[1]),
#                         text_colour=getRandColour(), 
#                         scroll_speed=0.1)

# def displayMessage(message, color="#ff0000", speed=0.1):
#     sense.show_message(message, text_colour=color, scroll_speed=speed)


#while True:
# pressure = ["Pressure", sense.get_pressure()]
# temperature = ["Temperature", sense.get_temperature()]
# humidity = ["Humidity", sense.get_humidity()]

# valuesStructs = [pressure, temperature, humidity]
# for valueStruct in valuesStructs:
#     display(valueStruct)