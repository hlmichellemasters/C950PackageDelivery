
class HashTable:
    def __init__(self, capacity):                             # default capacity of array is 100, if none passed in.
        self.array_size = capacity                        # if less than 100 capacity (number of packages), set to that.
        if capacity > 99:                                 # if more than 100 capacity (number of packages) is passed in,
            self.array_size = 100                         # then the capacity will be set to 100.
        self.array = [None for _ in range(self.array_size + 1)]

    def hash(self, key, collision_count=0):                       # start with collision count of zero.
        hash_code = (int(key) - 1) % self.array_size
        # print("the hashcode for key " + str(key) + " is " + str(hash_code))

        return hash_code + collision_count                    # if collisions, add collision num to the hash_code

    def insert_or_update(self, package):                                 # to assign a value to the hash table,
        index = self.hash(package.id)                                    # find an index from hashing the key
        # print("the index for package.id: " + str(package.id) + " is "  + str(index))
        hash_value = self.array[index]                                   # grab the value in that index.
        # print("the hash_value for the hash_array at index: " + str(index) + " is " + str(hash_value))

        if hash_value is None:                                        # if empty,
            self.array[index] = [index, package]                      # place new key-value pair
            # print("inserted into hashtable")
            return

        if hash_value[0] == index:                                       # if occupied with same key,
            self.array[index] = [index, package]                         # replace any current value with new value
            # print("updated hashtable")
            return

        # if neither of two above options, then collision!
        collision_number = 1

        while hash_value[0] != package.id:                               # while collisions continue,
            index = self.hash(package.id, collision_number)         # find new index to from key + collision number (>0)
            hash_value = self.array[index]                        # get new value at that index in the hash table

            if hash_value is None:
                self.array[index] = [index, package]
                return

            if hash_value[0] == package.id:
                self.array[index] = [index, package]
                return

            # if another collision increment the collision number one more and continue
            collision_number += 1

        return                                                     # return once the hash_value at the index is the key

    def find(self, package_id):                                             # to retrieve a given package by package id,
        # print("package_id passed is " + str(package_id))
        index = self.hash(package_id)                                     # hash the id to get an index
        # print("index found for that is: " + str(index))
        package_entry = self.array[index]                             # get the value at that index in the hash table
        # print("package found for that index is " + str(package_entry))

        if package_entry[1] is None:                                     # if none, then nothing to retrieve, return none.
            print("hash table found None?!")
            return None

        if int(package_entry[0] + 1) == int(package_id):                                   # if the value is the key
            return package_entry[1]                                   # return the key's value

        # if value is neither "none" nor key, then its a collision
        collisions = 1                                             # make collision counter --> 1
        print("package.id: " + str(package_id) + " had a collision at index " + str(index))

        while (package_entry[0] + 1) != int(package_id):                                   # while collisions continue,
            index = self.hash(package_id, collisions)                     # find new index using the id + collision (>0)
            package = self.array[index]                         # get the new value in the new index

            if package is None:
                return None

            if int(package_entry[0]) == int(package_id):
                return package_entry[1]

            # another collision!
            collisions += 1                                        # increment collision number and continue while loop

    def display_table(self):
        for x in range(self.array_size):
            print((str(x)) + " " + str(self.find(x)))
