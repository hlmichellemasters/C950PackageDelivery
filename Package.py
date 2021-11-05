class Package:
    def __init__(self, id, address, city, state, zip_code, delivery_deadline, mass_kg, special_notes=None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kg = mass_kg
        self.special_notes = special_notes
        self.location = "Hub"
        self.time_delivered = "N/A"

    def move_to_truck(self, truck):
        truck.packages_on_board.append(self)
        self.location = truck

    def deliver(self, time):
        self.location = "delivered"
        self.time_delivered = time

    def __str__(self):
        return '{:5s} {:40s} {:10s} {:20s} {:10s}'.format(self.id, self.address, self.delivery_deadline,
                                                          self.location, self.time_delivered)
