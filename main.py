from HashTable import HashTable
from Package import Package
from Truck import Truck
from math import inf
import csv

package_list = []
HUB_address = "4001 South 700 East"
num_packages = None


def load_package_data(package_data):
    with open(package_data) as package_file:   # open(package_data) as package_file,
        package_reader = csv.DictReader(package_file)
        package_count = 0

        for line in package_reader:
            new_package = Package(line['package_ID'], line['address'], line['city'], line['state'],
                                  line['zip_code'], line['delivery_deadline'], line['mass_kilo'],
                                  line['special_notes'])

            package_count += 1
            package_list.append(new_package)

    # create package hash table and insert all the packages
    package_hash = HashTable(package_count)
    for this_package in package_list:
        package_hash.insert_or_update(this_package)

    return package_hash, package_count


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
    # print("a1 idx:" + str(address1_index))
    address2_index = address_data.index(address2)
    # print("a2 idx:" + str(address2_index))
    distance = float(distance_data[address1_index][address2_index])

    return distance


# function to load trucks manually (according to specific instructions)
def load_truck(truck, selected_package=None):
    if len(truck.packages_on_board) == truck.max_packages:
        return "Truck is too full to load any more packages"
    if selected_package:
        package_index = package_list.index(selected_package)        # gets the index for the package in the package list
        package_to_load = package_list.pop(package_index)           # removes the package form the list to load it
        truck.packages_on_board.append(package_to_load)             # adds the package to the trucks list to deliver
        package_to_load.location = truck.name
        package_hashtable.insert_or_update(package_to_load)         # updates the hash table that holds package info


def auto_load_truck(truck, number_packages, available_package_list):
    for x in range(number_packages):
        if len(truck.packages_on_board) == truck.max_packages:
            return "Truck is too full to load any more packages"
        else:
            next_package_to_load = find_next_package(available_package_list, truck.current_last_package())
            package_to_load_index = available_package_list.index(next_package_to_load)
            available_package_list.pop(package_to_load_index)
            load_truck(truck, next_package_to_load)


# function to find the next package to load on a truck (loading in order to deliver in)
def find_next_package(available_packages, current_package=None):

    min_distance_max_priority = inf
    package_to_load_next = None

    if current_package is None:
        current_package_address = HUB_address
    else:
        current_package_address = current_package.address

    for this_package in available_packages:
        print(this_package)
        if this_package.delivery_deadline == "9:00 AM":
            priority_heuristic = -2
        elif this_package.delivery_deadline == "10:30 AM":
            priority_heuristic = -1
        else:
            priority_heuristic = 1

        distance_priority = distance_between(current_package_address, this_package.address) * priority_heuristic

        if (float(distance_priority) < float(min_distance_max_priority)) and (float(distance_priority) != 0.0):
            min_distance_max_priority = distance_priority
            package_to_load_next = this_package

    return package_to_load_next


distance_data = load_distance_data('DistancesOnly.csv')

address_data = load_address_data('AddressesOnly.csv')

package_hashtable, num_packages = load_package_data('PackageFile.csv')
print('number of packages is ' + str(num_packages))
# create the 3 trucks
truck1 = Truck('truck1')
truck2 = Truck('truck2')
truck3 = Truck('truck3')

# STRATEGY:
# 1) packages 13 (<10:30am), 14 (<10:30AM), 15 (<9:00 AM), 16 (<10:30AM), 19 (EOD) and 20 (<10:30AM)
#                              must all go together (putting on truck 2)
# 2) packages 3 (EOD), 18 (EOD), 36 (EOD), and 38 (EOD) must go on truck2
# 3) packages 6, 25, 28, and 32 cannot leave the hub before 9:05 a.m. and #9 cannot be delivered until > 10:20 AM)
#          (6 and 25 due < 10:30 AM)

# creating list to provide truck 2 with 1) and 2)
# giving the next highest priority 8 to truck 1 (without any special notes),
# (truck 1 will return after and get 3) + the rest of the packages
# fill list for truck 2 to 16 packages with next highest priority
# auto fill the trucks from these lists (then deliver them in that order)


# create list eligible for truck 1:
packages_for_truck_1 = []
for package in package_list:
    if package.special_notes == '':
        packages_for_truck_1.append(package)
print('number of packages available for truck 1 is ' + str(len(packages_for_truck_1)))     # should be 25?

# load truck 1
auto_load_truck(truck1, 8, packages_for_truck_1)
print("truck 1:")
truck1.display_num_packages()
updated_package_list = [package for package in package_list if package not in truck1.packages_on_board]
print('Updated package list has ' + str(len(updated_package_list)) + ' packages')

# load truck 2
# first pick out the 9 that are reserved for truck2 from the available package list
# then load the 7 non-selected packages (highest priority from available)

package_ids_for_truck_2 = [3, 13, 14, 15, 16, 19, 20, 18, 36, 38]               # picks out the 10 selected for truck 2
package_ids_not_for_truck_2 = [6, 25, 28, 32]                                   # picks out the 4 that can't leave yet
packages_for_truck2 = []
packages_not_for_truck2 = []

for package_id in package_ids_for_truck_2:                                      # finds the 10 packages
    packages_for_truck2.append(package_hashtable.find(package_id))              # and loads into a 'for' list

for package_id in package_ids_not_for_truck_2:                                  # finds the 4 packages
    packages_not_for_truck2.append(package_hashtable.find(package_id))          # and loads into a 'not for' list

# updates the "updated" package list by subtracting the 4 packages that can't go out yet.
updated_packages_for_truck2 = [package for package in updated_package_list if package not in packages_not_for_truck2]
# updates the list to not include the 10 we will specifically load later.
updated_packages_for_truck2 = [package for package in updated_packages_for_truck2 if package not in packages_for_truck2]

# loads the 16 - 10 (6) highest priority packages into truck2 (available packages without the 10 selected for truck2
auto_load_truck(truck2, (truck2.max_packages - len(package_ids_for_truck_2)), updated_packages_for_truck2)

print("truck 2:")
truck2.display_num_packages()

# updates the available package list to subtract the ones chosen for truck 2
updated_package_list = [package for package in package_list if package not in truck2.packages_on_board]

print('Updated package list has ' + str(len(updated_package_list)) + ' packages')



auto_load_truck(truck2, len(package_ids_for_truck_2), packages_for_truck2)      #
print("truck 2:")
truck2.display_num_packages()

updated_package_list.append(packages_not_for_truck2)                          #


# display table so far
# package_hashtable.display_table()

# load truck 3 (for driver in truck 1 to take when they get back)
auto_load_truck(truck3, 16, updated_package_list)
updated_package_list = [package for package in package_list if package not in truck1.packages_on_board]
print('Updated package list has ' + str(len(updated_package_list)) + ' packages')
# for each_package in truck2.packages_on_board:
#     print(each_package)


