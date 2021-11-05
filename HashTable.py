
class HashTable:
    def __init__(self, capacity=100):                             # default capacity of array is 100, if none passed in.
        self.array_size = capacity                        # if less than 100 capacity (number of packages), set to that.
        if capacity > 99:                                 # if more than 100 capacity (number of packages) is passed in,
            self.array_size = 100                         # then the capacity will be set to 100.
        self.array = [None for _ in range(self.array_size)]

    def hash(self, key, collision_count=0):                       # start with collision count of zero.
        key_bytes = key.encode()                                  # encode the key into bytes
        hash_code = sum(key_bytes)                                # convert to hash_code from bytes
        return (hash_code + collision_count) % self.array_size    # if collisions, add collision number to the hash_code

    def insert_or_update(self, package):                                 # to assign a value to the hash table,
        index = self.hash(package.id)                                    # find an index from hashing the key
        hash_value = self.array[index]                            # grab the value, if any in that index.

        if hash_value is None:                                    # if empty,
            self.array[index] = [package.id, package]                      # place new key-value pair
            return

        if hash_value[0] == package.id:                                  # if occupied with same key,
            self.array[index] = [package.id, package]                      # replace any current value with new value
            return

        # if neither of two above options, then collision!
        collision_number = 1

        while hash_value[0] != package.id:                               # while collisions continue,
            index = self.hash(package.id, collision_number)         # find new index to from key + collision number (>0)
            hash_value = self.array[index]                        # get new value at that index in the hash table

            if hash_value is None:
                self.array[index] = [package.id, package]
                return

            if hash_value[0] == package.id:
                self.array[index] = [package.id, package]
                return

            # if another collision increment the collision number one more and continue
            collision_number += 1

        return                                                     # return once the hash_value at the index is the key

    def find(self, id):                                       # to retrieve a given key,
        index = self.hash(id)                                     # hash the key to get an index
        hash_value = self.array[index]                             # get the value at that index in the hash table

        if hash_value is None:                                     # if none, then nothing to retrieve, return none.
            return None

        if hash_value[0] == id:                                   # if the value is the key
            return hash_value[1]                                   # return the key's value

        # if value is neither "none" nor key, then its a collision
        collisions = 1                                             # make collision counter --> 1

        while hash_value != id:                                   # while collisions continue,
            index = self.hash(id, collisions)                     # find new index using the key + collision (>0)
            hash_value = self.array[index]                         # get the new value in the new index

            if hash_value is None:
                return None

            if hash_value[0] == id:
                return hash_value[1]

            # another collision!
            collisions += 1                                        # increment collision number and continue while loop
