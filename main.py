from HashTable import HashTable
from Package import Package
from Truck import Truck
from math import inf
import csv

undelivered_package_list = []


def load_truck(truck, package_to_remove, package_hashtable):
    if len(truck.packages_on_board) == truck.max_packages:
        return "Truck is too full to load any more packages"
    package_to_load = undelivered_package_list.pop(package_to_remove)
    package_to_load.move_to_truck(truck)
    package_hashtable.insert_or_update(package_to_load)


def load_package_data(package_data):
    with open(package_data) as package_file:   # open(package_data) as package_file,
        package_reader = csv.DictReader(package_file)
        # distances_reader = csv.DictReader(distances_file)
        package_count = 0

        for line in package_reader:
            new_package = Package(line['package_ID'], line['address'], line['city'], line['state'],
                                  line['zip_code'], line['delivery_deadline'], line['mass_kilo'],
                                  line['special_notes'])

            package_count += 1
            undelivered_package_list.append(new_package)

    # create package hash table and insert all the packages
    package_hashtable = HashTable(package_count)
    for package in undelivered_package_list:
        package_hashtable.insert_or_update(package)

    return undelivered_package_list


# get the distances between all the locations
def load_distance_data(file):
    distance_list = []  # Define list "distance_data"
    with open(file) as distance_file:
        reader = csv.reader(distance_file)

        for line in reader:
            distance_list.append(line)

    return distance_list


def load_address_data(file):
    with open(file) as address_file:
        address_list = []
        reader = csv.reader(address_file)

        for line in reader:
            address_list = line

        return address_list


def distance_between(address1, address2):
    address1_index = address_data.index(address1)
    print("a1 idx:" + str(address1_index))
    address2_index = address_data.index(address2)
    print("a2 idx:" + str(address2_index))
    distance = distance_data[address1_index][address2_index]

    return distance


def min_distance_from(from_address, packages_on_truck):
    min_distance = inf
    for package in packages_on_truck:
        this_distance = distance_between(from_address, package.address)
        if (float(this_distance) < float(min_distance)) and (float(this_distance) != 0.0):
            min_distance = this_distance

    return min_distance


# alternative way to add the distance data to the packages themselves.
# with open('DistancesSimplified.csv', 'r') as distances_file:
#     reader = csv.DictReader(distances_file)
#
#     for line in reader:
#         # print("for line: ")
#         # print(line)
#         for package in undelivered_package_list:
#             # print("and for package: ")
#             # print(package)
#             if package.address == line["Address:"]:
#                 # print("a match is found with package: ")
#                 # print(package.id)
#                 found_package = package_hashtable.find(package.id)
#                 # print("found package:")
#                 # print(found_package)
#                 # print(type(found_package))
#                 package_ready = found_package.add_distances(line)
#                 # print("package ready?:")
#                 # print(package_ready)
#                 package_hashtable.insert_or_update(package_ready)
#                 package_ready.print_distances()
#                 break

distance_data = load_distance_data('DistancesOnly.csv')

address_data = load_address_data('AddressesOnly.csv')

undelivered_package_list = load_package_data('PackageFile.csv')

#test
print(distance_between("4001 South 700 East", "177 W Price Ave"))
print(min_distance_from("1330 2100 S", undelivered_package_list))


# create the 3 trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# packages 13, 14, 15, 16, 19 and 20 must all go together
# packages 3, 18, 36, and 38 must go on truck2
# packages 6, 25, 28, and 32 cannot leave the hub before 9:05 a.m. (6 and 25 due < 10:30 AM!!!)

# need to sort packages by the ones that need to be delivered the earliest
undelivered_package_list.sort(key=lambda x: x.delivery_deadline)
print("undelivered packages include:")
print(undelivered_package_list)

# print('{:10s} {:30s} {:10s} {:21s} {:20s}'.format("ID", "Destination", "Delivery Due",
#                                                   "Current Location", "Time Delivered"))
# print()
#
# for package in undelivered_package_list:
#     print(package)
