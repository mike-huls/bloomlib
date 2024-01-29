import dataclasses
import datetime

from bloomlib import BloomFilter

# bs = BloomSet(1000, 0.01)

bs = BloomFilter(expected_number_of_items=10000, desired_false_positive_rate=0.02)

bs.add()

bs.add(1)
bs.add('2')

assert bs.contains(1)


for i in range(300):
    bs.add(i)
assert bs.contains(0)
assert bs.contains(1)
assert bs.contains(299)
assert not bs.contains(300)

bs.add("mike")
print("contains string", bs.contains("mike"))
# print(help(bs))
# print(help(BloomSet))
bs.add_bulk(["aaa", "bbb", 1000, "3"])
print("added aaa, bbb and 1")
assert bs.contains(str(3))
assert bs.contains(1000)
assert not bs.contains("888")

print("current number of hashes", bs.get_number_of_hashes())
print("current number of bits", bs.get_number_of_bits())

# Contains dict
bs.add({'test': 'dict'})
print('contains dict', bs.contains({'test': 'dict'}))

# Contains date
now = datetime.datetime.now()
bs.add(now)
print('contains date ok', bs.contains(now))
print('contains date XX', bs.contains(datetime.datetime.now()))

@dataclasses.dataclass
class Person:
    name:str
    age:int

mike = Person(name='mike', age=34)
print(mike)

# Contains Data class
# bs.add(mike)
# print('contains mike', bs.contains(mike))

print(bs.get_number_of_hashes())