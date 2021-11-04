from HashTable import HashTable
from Package import Package
from Truck import Truck
import csv

with open('DistanceTable.csv', 'r') as package_file:
    reader = csv.DictReader(package_file)

    for line in reader:
        print(line)

# print(globals())
# hash_map = HashTable(15)
# hash_map.assign('gabbro', 'igneous')
# hash_map.assign('sandstone', 'sedimentary')
# hash_map.assign('gneiss', 'metamorphic')
# print(hash_map.retrieve('gabbro'))
# print(hash_map.retrieve('sandstone'))
# print(hash_map.retrieve('gneiss'))










