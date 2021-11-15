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
        # from instructions: The delivery status should report the package as at the hub, en route, or delivered.
        # Delivery status must include the time.
        self.delivery_status = "at the hub"

    def set_priority(self, priority):
        self.priority_heuristic = priority

        return "priority set to " + str(priority)

    def deliver(self, time):
        self.delivery_status = "delivered at " + str(time)

    def update_address(self, corrected_address):
        self.address = corrected_address[0]
        self.city = corrected_address[1]
        self.state = corrected_address[2]
        self.zip_code = corrected_address[3]

    def __str__(self):
        package_info = '{:3s} {:38s} {:9s} {:16s} {:6s} {:3s} {:20s} {:20s}'.format(self.id, self.address,
                                                                                    self.delivery_deadline, self.city,
                                                                                    self.zip_code, self.mass_kg,
                                                                                    self.delivery_status,
                                                                                    self.special_notes)
        return package_info
