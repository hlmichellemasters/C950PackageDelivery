import datetime


class Truck:
    def __init__(self, name, max_packages=16, speed_mph=18, time=8):
        self.name = name
        self.max_packages = max_packages
        self.speed_mph = speed_mph
        self.packages_on_board = []
        self.location = "Hub"
        self.miles_travelled = 0
        self.clock = datetime.datetime(1990, 1, 1, time, 0, 0, 0)
        self.completed_trips = 0

    def current_last_package(self):
        if self.packages_on_board:
            return self.packages_on_board[len(self.packages_on_board) - 1]

    def display_num_packages(self):
        print(self.name + " has " + str(len(self.packages_on_board)) + " packages on board")

    def get_new_time(self, distance_to_travel):
        seconds_to_deliver_rounded = int((distance_to_travel / 18) * 3600)
        time_delta = datetime.timedelta(seconds=seconds_to_deliver_rounded)
        self.clock = self.clock + time_delta
        print('clock for ' + self.name + ' is now ' + str(self.clock))
        return self.clock.strftime("%H:%M")

    def increment_trip_count(self):
        self.completed_trips += 1
        print("incremented trip count for " + self.name)








