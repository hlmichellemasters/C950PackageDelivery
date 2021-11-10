class Package:
    def __init__(self, package_id, address, city, state, zip_code, region, delivery_deadline, mass_kg,
                 special_notes):

        self.id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kg = mass_kg
        self.special_notes = special_notes
        self.priority_heuristic = 0
        self.region = region
        self.location = "Hub"
        self.time_delivered = "N/A"

    def set_priority(self, priority):
        self.priority_heuristic = priority

        return "priority set to " + str(priority)

    def deliver(self, time):
        self.location = "delivered"
        self.time_delivered = time

    def __str__(self):
        package_info = '{:5s} {:40s} {:10s} {:20s} {:10s} {:10s} {:10s}'.format(self.id, self.address,
                                                                                self.delivery_deadline,
                                                                                self.location, self.region,
                                                                                self.time_delivered,
                                                                                self.special_notes)
        return package_info
