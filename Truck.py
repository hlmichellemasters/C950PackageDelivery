from Package import Package

class Truck:
    def __init__(self, name, max_packages=16, speed_mph=18):
        self.name = name
        self.max_packages = max_packages
        self.speed_mph = speed_mph
        self.packages_on_board = []
        self.location = "Hub"
        self.miles_travelled = 0

    def current_last_package(self):
        if self.packages_on_board:
            return self.packages_on_board[len(self.packages_on_board) - 1]

    def display_num_packages(self):
        print(self.name + " has " + str(len(self.packages_on_board)) + " packages on board")

