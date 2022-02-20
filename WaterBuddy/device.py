from helper_functions import sensehat

class WaterBuddy:
    def __init__(self):
        pass

    def main(self):
        print("Device Established...")
        sensehat.displayMessage("Device Established...")


if __name__ == "__main__":
    water_buddy = WaterBuddy()
    water_buddy.main()