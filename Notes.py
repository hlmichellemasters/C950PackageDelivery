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