import datetime

from HashTable import HashTable
from Package import Package
from Truck import Truck
from math import inf
import csv
import operator

total_available_package_list = []
package_hashtable = {}
HUB_address = "4001 South 700 East"
num_packages = None
total_mileage = 0
start_time = datetime.datetime(1990, 1, 1, 8, 0, 0, 0)
current_time = datetime.datetime(1990, 1, 1, 8, 0, 0, 0)
last_packages_available_time = datetime.datetime(1990, 1, 1, 9, 5, 0, 0)
returned_for_late_priority_packages = False
truck1 = Truck('truck1')
truck2 = Truck('truck2')


def get_time():
    global total_mileage, start_time, current_time
    seconds_to_deliver_rounded = int((total_mileage / 18) * 3600)
    time_delta = datetime.timedelta(seconds=seconds_to_deliver_rounded)
    current_time = start_time + time_delta
    print('current time is ' + str(current_time))


def update_time_check_print():
    global package_hashtable, current_time
    get_time()
    print("The time is now: " + str(current_time))
    package_hashtable.display_table()


def load_package_data(package_data):
    global total_available_package_list, package_hashtable
    with open(package_data) as package_file:  # open(package_data) as package_file,
        package_reader = csv.DictReader(package_file)
        package_count = 0

        for line in package_reader:
            new_package = Package(line['package_ID'], line['address'], line['city'], line['state'],
                                  line['zip_code'], line['delivery_deadline'], line['mass_kilo'],
                                  line['special_notes'])

            package_count += 1
            total_available_package_list.append(new_package)

    # create package hash table and insert all the packages
    package_hashtable = HashTable(package_count)
    for this_package in total_available_package_list:
        package_hashtable.insert_or_update(this_package)

    package_hashtable.display_table()

    return package_count


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
    address2_index = address_data.index(address2)
    distance = float(distance_data[address1_index][address2_index])

    return distance


# function to load truck by package
def load_truck(truck, selected_package):
    # print("total available packages are: ")
    # for package in total_available_package_list:
    #     print(package)
    #
    # print("selected_package is " + str(print(selected_package)))

    package_index = total_available_package_list.index(selected_package)  # gets index of package in the list
    package_to_load = total_available_package_list.pop(package_index)  # removes package from list to load it
    truck.packages_on_board.append(package_to_load)  # adds package to trucks list to deliver
    package_to_load.location = truck.name  # updates package location to truck (name)
    package_hashtable.insert_or_update(package_to_load)  # updates hash table that holds package info


def add_packages_to_list(package_ids_to_add):
    list_to_return = []
    for package_id in package_ids_to_add:
        package_to_add = package_hashtable.find(package_id)
        list_to_return.append(package_to_add)

    return list_to_return


# STRATEGY:
# 1) packages 13 (<10:30am), 14 (<10:30AM), 15 (<9:00 AM), 16 (<10:30AM), 19 (EOD) and 20 (<10:30AM)
#                              must all go together (putting on truck 1?)
# 2) packages 3 (EOD), 18 (EOD), 36 (EOD), and 38 (EOD) must go on truck2
# 3) packages 6, 25, 28, and 32 cannot leave the hub before 9:05 a.m. and #9 cannot be delivered until > 10:20 AM)
#          (6 and 25 due < 10:30 AM)
# will create an "effectively" available list for each truck1 and truck2 for each return

def auto_load_truck(truck):
    global total_available_package_list

    package_ids_only_truck2 = [3, 18, 36, 38]
    package_ids_only_truck1 = [13, 14, 15, 16, 19, 20]
    package_ids_not_before_9 = [6, 9, 25, 28, 32]

    packages_only_truck2 = add_packages_to_list(package_ids_only_truck2)
    packages_only_truck1 = add_packages_to_list(package_ids_only_truck1)
    packages_not_before_9 = add_packages_to_list(package_ids_not_before_9)

    effectively_available_package_list = total_available_package_list

    if truck.clock < datetime.datetime(1990, 1, 1, 9, 5, 0, 0):  # if time before 9:05 AM can't 6, (9?), 25, 28, 32
        effectively_available_package_list = [package for package in total_available_package_list if
                                              package not in packages_not_before_9]

    # for truck 1, going to go ahead and just load all of the packages that need to go together,
    # then the truck will be filled the rest of the way with the packages that are highest priority and available.
    if truck.name == 'truck1':
        effectively_available_package_list = [package for package in effectively_available_package_list if
                                              package not in packages_only_truck2]

    # for truck 2, going to offer all of the "truck 2 only" packages, but not require truck 2 to take on first delivery
    if truck.name == 'truck2':
        effectively_available_package_list = [package for package in effectively_available_package_list if
                                              package not in packages_only_truck1]

    # finishes filling both trucks.
    while len(truck.packages_on_board) < truck.max_packages and effectively_available_package_list:
        # print("truck's current last package is " + str(truck.current_last_package()))
        # print("effectively available packages for " + truck.name + " are: ")
        # for package in effectively_available_package_list:
        #     print(package)
        # print("end of print")
        next_package_to_load = find_next_package(effectively_available_package_list, truck.current_last_package())
        # print("next_package_to_load is " + str(next_package_to_load))
        package_to_load_index = effectively_available_package_list.index(next_package_to_load)
        effectively_available_package_list.pop(package_to_load_index)  # remove from temp eff. available packages
        load_truck(truck, next_package_to_load)

    reorder_packages(truck)
    print(truck.name + " is full with  " + str(len(truck.packages_on_board)) + " packages")
    print('Total available packages is now ' + str(len(total_available_package_list)))
    print("Here is a list and order of the packages in " + truck.name)
    for package in truck.packages_on_board:
        print(package)


# function to find the next package to load on a truck (loading in order to deliver in)
def find_next_package(available_packages, current_package):
    min_distance_max_priority = inf
    package_to_load_next = None

    if current_package is None:
        current_package_address = HUB_address
    else:
        current_package_address = current_package.address

    for this_package in available_packages:
        print(this_package)
        priority_heuristic = 1
        if this_package.delivery_deadline == "9:00 AM":
            priority_heuristic = -2
        if this_package.delivery_deadline == "10:30 AM":
            priority_heuristic = -1

        distance_priority = distance_between(current_package_address, this_package.address) * priority_heuristic

        if (float(distance_priority) < float(min_distance_max_priority)) and (float(distance_priority) != 0.0):
            min_distance_max_priority = distance_priority
            this_package.set_priority(distance_priority)
            package_to_load_next = this_package

    return package_to_load_next


def reorder_packages(truck):
    truck.packages_on_board.sort(key=operator.attrgetter("priority_heuristic"))
    print("Now printing the order of the packages on board:")
    for package in truck.packages_on_board:
        print(package)
    print("end of print")
    print("Auto re-ordered packages before leaving the hub")


def truck_deliver_packages(truck):

    while truck.packages_on_board:
        global last_packages_available_time
        global returned_for_late_priority_packages

        if truck.clock >= last_packages_available_time and not returned_for_late_priority_packages:
            truck_return_to_hub(truck)
            print(truck.name + " clock says " + str(truck.clock))
            returned_for_late_priority_packages = True

        in_route_package = truck.packages_on_board.pop(0)
        if truck.location == 'Hub':
            truck_address = HUB_address
        else:
            truck_address = truck.location

        distance_to_travel = distance_between(truck_address, in_route_package.address)
        global total_mileage
        total_mileage = total_mileage + distance_to_travel
        delivery_time = truck.get_new_time(distance_to_travel)
        truck.location = in_route_package.address
        in_route_package.location = 'Delivered by ' + str(truck.name)
        in_route_package.time_delivered = delivery_time
        package_delivered = in_route_package
        package_hashtable.insert_or_update(package_delivered)
        update_time_check_print()

    print(truck.name + ' delivered all of their packages')

    truck_return_to_hub(truck)


def truck_return_to_hub(truck):
    if truck.location == 'Hub':
        return
    distance_to_travel = distance_between(truck.location, HUB_address)
    global total_mileage
    total_mileage = total_mileage + distance_to_travel
    truck.get_new_time(distance_to_travel)
    truck.increment_trip_count()


def start_delivery():
    while total_available_package_list:
        auto_load_truck(truck1)
        auto_load_truck(truck2)

        truck_deliver_packages(truck1)
        truck_deliver_packages(truck2)

        print(truck1.name + ' location: ' + truck1.location)
        print(truck2.name + ' location: ' + truck2.location)


# Main program begins
distance_data = load_distance_data('DistancesOnly.csv')

address_data = load_address_data('AddressesOnly.csv')

num_packages = load_package_data('PackageFile.csv')

print('number of packages is ' + str(num_packages))

start_delivery()

# # # display table so far
package_hashtable.display_table()
print('Total mileage: ' + str(total_mileage))
print('truck1 made ' + str(truck1.completed_trips) + " trips")
print('truck2 made ' + str(truck2.completed_trips) + " trips")
