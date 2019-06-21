__author__ = 'NJORO'

from my_math.Primes import nearest_high_prime


class HashTable:
    def __init__(self, data_size=0):
        self._size = nearest_high_prime(data_size)
        self._slots = [None] * self._size
        self._data = [None] * self._size

    def hash_function(self, key):
        return key % self._size

    def rehash(self, old_hash):
        return (old_hash + 1) % self._size  # linear prob with step 1. todo add different prob techniques

    def store(self, hash_value, key, data, chain=False):
        if self._slots[hash_value] is None:  # slot is empty
            self._slots[hash_value] = key
            self._data[hash_value] = data
            return True
        elif self._slots[hash_value] == key:  # replace data is key is same
            self._data[hash_value] = data
            return True
        elif chain:  # chain.
            return True  # todo chain
        else:  # need a rehash
            return False

    def put_pair(self, pair):
        if len(pair) != 2:
            raise AssertionError("List item {} should be [key, value] pair.".format(pair))
        self.put(pair[0], pair[1])

    def put(self, key, data):
        hash_value = self.hash_function(key)

        if not self.store(hash_value, key, data):
            next_slot = self.rehash(hash_value)
            while self._slots[next_slot] is not None and self._slots[next_slot] != key:
                next_slot = self.rehash(next_slot)  # todo implement break on return to initial slot
            self.store(next_slot, key, data)

    def get(self, key):
        start_slot = self.hash_function(key)

        data, found, current_slot = None, False, start_slot
        while self._slots[current_slot] is not None and not found:  # stop if empty slot or key found
            if self._slots[current_slot] == key:
                found = True
                data = self._data[current_slot]
            else:
                current_slot = self.rehash(current_slot)
                if current_slot == start_slot:
                    break  # stop if rehash returns to start slot
        return data

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, data):
        self.put(key, data)

    def __repr__(self):
        text = "HashTable(size = {}) => \n".format(self._size)
        for slot_data_pair in zip(self._slots, self._data):
            text += "[{}, {}], \n".format(slot_data_pair[0], slot_data_pair[1])
        return text


    @classmethod
    def hash(cls, key_value_list):
        h = cls(len(key_value_list))
        for pair in key_value_list:
            h.put_pair(pair)
        return h


if __name__ == "__main__":
    list = [[54,    "Cata"],
            [70,    "Catb"],
            [301,   "Catc"],
            [27,    "Catd"],
            [342,   "Cate"],
            [182,   "Catf"],
            [33,    "Catg"],
            [978,   "Cath"],
            [45,    "Cati"],
            [111,   "Catj"],
            [73,    "Catk"],
            [20,    "Catl"]]
    h = HashTable.hash(list)
    # h.put_pair(list[1])
    # h.put_pair(list[1])
    # h.put_pair(list[2])
    # h.put_pair(list[3])
    print(h)
    print(h.get(301))
