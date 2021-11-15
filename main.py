# Heaven-Leigh Michelle Masters
# Student ID: 001328444
#
import datetime
import copy
import DataLoader
from Truck import Truck
from math import inf

# holds the HUB's address
HUB_address = "4001 South 700 East"

# # initiator of number of packages
# num_packages = None

# initiator of the total mileage driven
total_mileage = 0

# delivery start time
start_time = datetime.datetime(1990, 1, 1, 8, 0, 0, 0)

# initiator of current time
current_time = datetime.datetime(1990, 1, 1, 8, 0, 0, 0)

# time that the late packages are available to be picked up
last_packages_available_time = datetime.datetime(1990, 1, 1, 9, 5, 0, 0)

# time that package 9's address correction will occur
package_9_address_correction_time = datetime.datetime(1990, 1, 1, 10, 20, 0, 0)
# address that package 9 will be corrected to:
package_9_correct_address = ["410 S State St", "Salt Lake City", "UT", "84111"]

# initiator of the timestamp dictionary
timestamps = {}

# initiators of the effectively 2 trucks
truck1 = Truck('truck1')
truck2 = Truck('truck2')


# updates the current time with truck time (if ahead) and takes a snapshot of the package hash table at the current time
def timestamp(truck_time):
    global current_time

    if truck_time > current_time:
        current_time = truck_time

    time_string = "" + str(current_time.hour) + ":" + str(current_time.minute)
    current_package_info = copy.deepcopy(package_hashtable)
    print("The time is now: " + time_string + " saved the package hash table info for this time")
    timestamps[time_string] = current_package_info
    print("key is " + time_string + " and the packageHashTable is:")
    package_hashtable.display_table()


def display_timestamp(hour, minute):
    hr = hour
    min = minute
    time_key = "" + str(hr) + ":" + str(min)
    found_timestamp = False
    while not found_timestamp:
        packages_info_at_that_time = timestamps.get(time_key)
        if packages_info_at_that_time is None:
            print("didn't find that exact time")
            if min > 0:
                min = min - 1
            else:
                hr = hr - 1
                min = 59
            time_key = ("" + str(hr) + ":" + str(min))
            print("current time_key is " + time_key)
        else:
            found_timestamp = True
            packages_info_at_that_time.display_table()

    print("subtracted one minute to look again")
    print("found_timestamp is : " + str(found_timestamp))


def distance_between(address1, address2):
    address1_index = address_data.index(address1)
    address2_index = address_data.index(address2)
    distance = float(distance_data[address1_index][address2_index])

    return distance


# function to load truck by package
def load_truck(truck, package_id):
    global package_hashtable, total_available_package_list

    print("package id is " + str(package_id))
    package_to_load = package_hashtable.find(package_id)  # copies package from hashtable to load truck by package ID

    print("package to load is: " + str(package_to_load))
    truck.packages_on_board.append(package_to_load)  # adds package to trucks list to deliver
    package_to_load.delivery_status = "enroute with + " + truck.name  # updates package location to truck (name)
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
    global total_available_package_list, current_time, last_packages_available_time

    print("loading: " + truck.name)
    package_ids_only_truck2 = [3, 18, 36, 38]
    package_ids_go_together = [13, 14, 15, 16, 19, 20]
    package_ids_not_before_9 = [6, 25, 28, 32]
    package_ids_not_before_10 = [9]

    packages_only_truck2 = add_packages_to_list(package_ids_only_truck2)
    packages_only_go_together = add_packages_to_list(package_ids_go_together)
    packages_not_before_9 = add_packages_to_list(package_ids_not_before_9)
    packages_not_before_10 = add_packages_to_list(package_ids_not_before_10)

    packages_north_central = []
    packages_south_west = []

    for package in total_available_package_list:
        if package.region == "N" or package.region == "C":
            packages_north_central.append(package)
        else:
            packages_south_west.append(package)

    packages_not_priority = []
    for package in total_available_package_list:
        if package.delivery_deadline != "EOD":
            packages_not_priority.append(package)

    effectively_available_package_list = total_available_package_list

    print("current time " + str(current_time) + "last packages available time is " + str(last_packages_available_time))
    if current_time < package_9_address_correction_time:
        effectively_available_package_list = [package for package in total_available_package_list if
                                              package not in packages_not_before_10]

        if current_time < last_packages_available_time:  # if time before 9:05 AM can't deliver 6, (9?), 25, 28, 32
            effectively_available_package_list = [package for package in effectively_available_package_list if
                                                  package not in packages_not_before_9]

        print("the effective packages for delivery before 9:05am is: ")
        for package in effectively_available_package_list:
            print(package)

    if truck.name == 'truck1':
        effectively_available_package_list = [package for package in effectively_available_package_list if
                                              package not in packages_only_truck2]
        effectively_available_package_list = [package for package in effectively_available_package_list if
                                              package not in packages_only_go_together]
        effectively_available_package_list = [package for package in effectively_available_package_list if
                                              package not in packages_north_central]

    # finishes filling both trucks.
    while (len(truck.packages_on_board) < truck.max_packages) and effectively_available_package_list:
        next_package_id_to_load = find_next_package(effectively_available_package_list, truck.current_last_package())

        load_truck(truck, next_package_id_to_load)

        next_package_to_load = package_hashtable.find(next_package_id_to_load)
        remove_id_from_effective_list = effectively_available_package_list.index(next_package_to_load)
        effectively_available_package_list.pop(remove_id_from_effective_list)

    # update the total available packages list:
    total_available_package_list = [package for package in total_available_package_list if package not in
                                    truck.packages_on_board]

    print(truck.name + " is full with  " + str(len(truck.packages_on_board)) + " packages")
    print(truck.name + " has had " + str(truck.num_high_priority_packages) + " high priority packages")
    print('Total available packages is now ' + str(len(total_available_package_list)))
    print(
        "Here is a list and order of the packages in " + truck.name + " on delivery " + str(truck.completed_trips + 1))
    for package in truck.packages_on_board:
        print(package)


# function to find the next package to load on a truck (loading in order to deliver in)
def find_next_package(available_packages, current_package):
    min_distance_max_priority = inf

    if current_package is None:
        current_package_address = HUB_address
        print("current package is None!")
    else:
        current_package_address = current_package.address

    for this_package in available_packages:
        priority_heuristic = 1
        distance = distance_between(current_package_address, this_package.address)

        if this_package.delivery_deadline == "9:00 AM":
            priority_heuristic = .1
        if this_package.delivery_deadline == "10:30 AM":
            priority_heuristic = .3

        distance_priority = distance * priority_heuristic

        if distance == 0:
            package_to_load_next = this_package

        elif float(distance_priority) < float(min_distance_max_priority):
            min_distance_max_priority = distance_priority
            this_package.set_priority(distance_priority)
            package_to_load_next = this_package

    package_id_to_load = package_to_load_next.id

    return package_id_to_load


def truck_deliver_packages(truck):
    global total_mileage, package_9_address_correction_time
    while truck.packages_on_board:

        in_route_package = truck.packages_on_board.pop(0)

        if truck.location == 'Hub':
            truck_address = HUB_address
        else:
            truck_address = truck.location

        # #9 address will be corrected to 410 S State St., Salt Lake City, UT 84111 at 10:20am
        if int(in_route_package.id) == 9 and truck.clock < package_9_address_correction_time:
            # so if the current package is #9 and its before the correction time,
            # append the package on to the packages on board of the truck (adds to end of truck's delivery list)
            truck.packages_on_board.append(in_route_package)
            # if there is more than 1 package on board, continue delivering
            if len(truck.packages_on_board) > 1:
                continue
            # otherwise return to the hub to get more packages
            else:
                truck.return_to_hub(distance_to_travel)

        if int(in_route_package.id) == 9 and truck.clock > package_9_address_correction_time:
            # if current package is #9 and its past the correction time,
            # then update the packages address
            in_route_package.update_address(package_9_correct_address)

        # find the distance between the truck's current location adn the package's destination address
        distance_to_travel = distance_between(truck_address, in_route_package.address)

        # increment the total mileage for the day with that distance
        total_mileage = total_mileage + distance_to_travel
        # find the delivery time of the package by updating the truck's clock with the distance travelled
        delivery_time = truck.get_new_time(distance_to_travel)
        # update the truck's location to the that package's address
        truck.location = in_route_package.address
        # update the delivery status of the package
        in_route_package.delivery_status = 'Delivered by ' + str(truck.name) + " at " + str(delivery_time)
        # call this package the delivered package now
        package_delivered = in_route_package
        # and update the hashtable for that package
        package_hashtable.insert_or_update(package_delivered)
        # take a timestamp of the packages information at that time, to use for looking up timestamps later
        timestamp(truck.clock)

    print(truck.name + ' delivered all of their packages')

    # when truck is empty, update the total mileage with the miles required to return to hub
    distance_to_travel = distance_between(truck.location, HUB_address)
    # return the truck to the hub
    truck.return_to_hub(distance_to_travel)
    # update the total mileage for the day with that distance as well
    total_mileage = total_mileage + distance_to_travel


# # # Main program

# load the distance data (a table which holds the distances between each address)
distance_data = DataLoader.load_distance_data('DistancesOnly.csv')

# load the address data (a list which shows the index for each address in the distance data)
address_data = DataLoader.load_address_data('AddressesOnly.csv')

# load the package data (and also import the number of packages, a list of all the packages, and the hashtable of them
num_packages, total_available_package_list, package_hashtable = DataLoader.load_package_data('PackageFile.csv')

# take a starting timestamp of the package information
timestamp(start_time)

# while there are still packages to deliver, keep loading and delivering each truck
while total_available_package_list:
    auto_load_truck(truck1)
    auto_load_truck(truck2)
    truck_deliver_packages(truck1)
    truck_deliver_packages(truck2)

# take a final timestamp for the end of the day
end_time = current_time
timestamp(end_time)
# # # display table
package_hashtable.display_table()
print('Total packages left to deliver is: ' + str(len(total_available_package_list)))
print('Total mileage: ' + str(total_mileage))
print('The time is now: ' + str(end_time))
print('truck1 made ' + str(truck1.completed_trips) + " trips")
print('truck2 made ' + str(truck2.completed_trips) + " trips")

test_info_at_that_time = timestamps.get("8:0")
print("displaying test table")
test_info_at_that_time.display_table()
# # # command line interface

print("****** Welcome to the Western Governors University Package Service! ******\n\n")
print("The day started at 8:00 am (or 8 hours and 0 minutes)")
print("The deliveries were done at " + str(end_time))
print("I can show you the statuses of all the packages at any given time during the delivery day")
print("Press any non-number (such as a letter) to exit the program")

while True:
    try:
        hour = int(input("What hour would you like to look at a timestamp of the packages for?"))
        minute = int(input("What minute would you like to look at a timestamp of the packages for?"))
        display_timestamp(hour, minute)
    except ValueError:
        print("You entered a non-number, now exiting the program")
        exit()

