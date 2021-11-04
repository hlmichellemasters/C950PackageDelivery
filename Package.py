
class Package:
    def __init__(self, address, city, state, zip_code, delivery_deadline, mass_kg, special_notes=None):
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.mass_kg = mass_kg
        self.special_notes = special_notes
        self.location = "Hub"
        self.time_delivered = None




