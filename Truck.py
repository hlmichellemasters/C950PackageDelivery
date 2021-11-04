
class Truck:
    def __init__(self, max_packages=16, speed_mph=18):
        self.max_packages = max_packages
        self.speed_mph = speed_mph
        self.packages_on_board = []
        self.location = "Hub"
