import datetime

HUB_address = "4001 South 700 East"


class Truck:
    def __init__(self, name, max_packages=7, speed_mph=18, hour_time=8, minute_time=0):
        self.name = name
        self.max_packages = max_packages
        self.speed_mph = speed_mph
        self.packages_on_board = []
        self.location = "Hub"
        self.miles_travelled = 0
        self.clock = datetime.datetime(1990, 1, 1, hour_time, minute_time, 0, 0)
        self.completed_trips = 0
        self.num_high_priority_packages = 0

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
        self.max_packages = 16

    def return_to_hub(self, distance_to_travel):
        if self.location == 'Hub':
            return
        self.get_new_time(distance_to_travel)
        self.increment_trip_count()










