import random
import time
import timeit
from typing import List

import bloomlib
print(dir(bloomlib))
print(help(bloomlib))

from bloomlib import BloomFilter
from bloomset_rs.test.utils.timing import display_times, Timing, performance_check
from bloomset_rs.test.utils.utils_for_testing import random_str

LANGUAGE = "RUST"

def test_time_add():
    """ """
    strt = time.perf_counter()
    for elem_count in [10]:
    # for elem_count in [10, 1_000, 100_000]:
        bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
        string_list = [random_str(16) for _ in range(elem_count)]
        int_list = [random.randint(a=0, b=1000) for _ in range(elem_count)]
        number = 3
        repeat = 5
        timings_strings: [float] = timeit.repeat(stmt=f"func({string_list})", globals={'func': bloom.add_bulk}, number=number, repeat=repeat)
        timings_ints: [float] = timeit.repeat(stmt=f"func({int_list})", globals={'func': bloom.add_bulk}, number=number, repeat=repeat)

        print('\n')
        display_times([
            Timing(name=f'{elem_count} strings', times=[t * 1_000 for t in timings_strings], size=None),
            Timing(name=f'{elem_count} ints', times=[t * 1_000 for t in timings_ints], size=None),
        ], name=f"{LANGUAGE} add_bulk (#{len(string_list)})", decimals=9)
    print(time.perf_counter() - strt)

def test_time_contains():
    """ """
    elem_count = 1_000

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    string_list = [random_str(16) for _ in range(elem_count)]
    first_string = string_list[0]
    int_list = [random.randint(a=0, b=1000) for _ in range(elem_count)]
    bloom.add_bulk(int_list)
    bloom.add_bulk(string_list)
    number = 3
    repeat = 5
    t_contains_string_exists: [float] = timeit.repeat(stmt=f"func('{first_string}')", globals={'func': bloom.contains}, number=number, repeat=repeat)
    t_contains_string_not_exists: [float] = timeit.repeat(stmt=f"func('zz')", globals={'func': bloom.contains}, number=number, repeat=repeat)
    t_contains_int_exists: [float] = timeit.repeat(stmt=f"func(500)", globals={'func': bloom.contains}, number=number, repeat=repeat)
    t_contains_int_not_exists: [float] = timeit.repeat(stmt=f"func(100_000)", globals={'func': bloom.contains}, number=number, repeat=repeat)

    print('\n')
    display_times([
        Timing(name=f'contains string', times=[t * 1_000 for t in t_contains_string_exists], size=None),
        Timing(name=f'contains unknown string', times=[t * 1_000 for t in t_contains_string_not_exists], size=None),
        Timing(name=f'contains int', times=[t * 1_000 for t in t_contains_int_exists], size=None),
        Timing(name=f'contains unknown int', times=[t * 1_000 for t in t_contains_int_not_exists], size=None),
    ], name=f"{LANGUAGE} Contains (#{len(string_list)})", decimals=9)


def test_performance_check():
    elem_count = 1000
    string_list = [random_str(16) for _ in range(elem_count)]
    int_list = [random.randint(a=0, b=1000) for _ in range(elem_count)]

    @performance_check
    def _bulk_add_strings(bloom:BloomFilter, add_this_list:List):
        bloom.add_bulk(add_this_list)

    @performance_check
    def _bulk_add_ints(bloom:BloomFilter, add_this_list:List):
        bloom.add_bulk(add_this_list)


    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)
    _bulk_add_strings(bloom=bloom, add_this_list=string_list)
    _bulk_add_strings(bloom=bloom, add_this_list=int_list)

def test_limits_add_one_by_one():
    elem_count = 100_000_000
    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)

    print("memsize (bits):", bloom.get_number_of_bits())
    print("nhashes:", bloom.get_number_of_hashes())

    return
    strt = time.perf_counter()
    for i in range(elem_count):
        bloom.add(i)
    endd = time.perf_counter()
    print(f"added {elem_count} items in {(endd - strt) * 1000}ms")

    strt = time.perf_counter()
    res = bloom.contains(elem_count-1)
    endd = time.perf_counter()
    print(f"checked {elem_count-1}? (={res}) in {(endd - strt) * 1000}ms")

    strt = time.perf_counter()
    res = bloom.contains(elem_count+1)
    endd = time.perf_counter()
    print(f"checked {elem_count+1}? (={res}) in {(endd - strt) * 1000}ms")

def test_limits_add_bulk():
    elem_count = 100_000_000
    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)

    print("memsize (bits):", bloom.get_number_of_bits())
    print("nhashes:", bloom.get_number_of_hashes())

    the_list = list(range(elem_count))

    strt = time.perf_counter()
    bloom.add_bulk(the_list)
    endd = time.perf_counter()
    print(f"added {elem_count} items in {(endd - strt) * 1000}ms")

    strt = time.perf_counter()
    res = bloom.contains(elem_count-1)
    endd = time.perf_counter()
    print(f"checked {elem_count-1}? (={res}) in {(endd - strt) * 1000}ms")

    strt = time.perf_counter()
    res = bloom.contains(elem_count+1)
    endd = time.perf_counter()
    print(f"checked {elem_count+1}? (={res}) in {(endd - strt) * 1000}ms")


