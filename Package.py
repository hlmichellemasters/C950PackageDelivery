class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, mass_kg,
                 distances=None, special_notes=None):
        if distances is None:
            distances = {}
        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kg = mass_kg
        self.special_notes = special_notes
        self.location = "Hub"
        self.time_delivered = "N/A"
        self.distances = distances

    def add_distances(self, distances):
        self.distances = distances
        return self

    def print_distances(self):
        for key, value in self.distances.items():
            print(key, ' : ', value)

    def move_to_truck(self, truck):
        truck.packages_on_board.append(self)
        self.location = truck

    def deliver(self, time):
        self.location = "delivered"
        self.time_delivered = time

    def __str__(self):
        package_info = '{:5s} {:40s} {:10s} {:20s} {:10s}'.format(self.id, self.address, self.delivery_deadline,
                                                                  self.location, self.time_delivered)

        return package_info
