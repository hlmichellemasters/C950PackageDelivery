from HashTable import HashTable
from Package import Package
import csv


# loads the package data from the csv file
def load_package_data(package_data):
    total_available_package_list = []
    with open(package_data) as package_file:  # open(package_data) as package_file,
        package_reader = csv.DictReader(package_file)
        package_count = 0

        for line in package_reader:
            new_package = Package(line['package_ID'], line['address'], line['city'], line['state'],
                                  line['zip_code'], line['region'], line['delivery_deadline'], line['mass_kilo'],
                                  line['special_notes'])

            package_count += 1
            total_available_package_list.append(new_package)

            # create package hash table and insert all the packages
            package_hashtable = HashTable(package_count)
            for this_package in total_available_package_list:
                package_hashtable.insert_or_update(this_package)

    package_hashtable.display_table()

    return package_count, total_available_package_list, package_hashtable


# get the distances between all the locations
def load_distance_data(file):
    distance_list = []  # Define list "distance_data"
    with open(file) as distance_file:
        reader = csv.reader(distance_file)

        for line in reader:
            distance_list.append(line)

    return distance_list


# loads the address data from the csv file
def load_address_data(file):
    with open(file) as address_file:
        address_list = []
        reader = csv.reader(address_file)

        for line in reader:
            address_list = line

        return address_list
