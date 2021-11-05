from HashTable import HashTable
from Package import Package
from Truck import Truck
import csv


undelivered_package_list = []

def load_truck(truck, package_to_remove):
    if len(truck.packages_on_board) == truck.max_packages:
        return "Truck is too full to load any more packages"
    package_to_load = undelivered_package_list.pop(package_to_remove)
    package_to_load.move_to_truck(truck)
    package_hashtable.insert_or_update(package_to_load)


with open('PackageFile.csv', 'r') as package_file:
    reader = csv.DictReader(package_file)
    package_count = 0

    for line in reader:
        package = Package(line['package_ID'], line['address'], line['city'], line['state'],
                          line['zip_code'], line['delivery_deadline'], line['mass_kilo'],
                          line['special_notes'],)
        package_count += 1
        undelivered_package_list.append(package)

# create package hash table and insert all the packages
package_hashtable = HashTable(package_count)

for package in undelivered_package_list:
    package_hashtable.insert_or_update(package)

# get the distances between all the locations
with open('DistanceTable.csv', 'r') as distances_file:
    reader = csv.DictReader(distances_file)

    for line in reader:
        dictionary = {}

# create the 3 trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# packages 13, 14, 15, 16, 19 and 20 must all go together
# packages 3, 18, 36, and 38 must go on truck2
# packages 6, 25, 28, and 32 cannot leave the hub before 9:05 a.m. (6 and 25 due < 10:30 AM!!!)

# need to sort packages by the ones that need to be delivered the earliest
undelivered_package_list.sort(key=lambda x: x.delivery_deadline)

print('{:10s} {:30s} {:10s} {:21s} {:20s}'.format("ID", "Destination", "Delivery Due",
                                                  "Current Location", "Time Delivered"))
print()

for package in undelivered_package_list:
    print(package)



