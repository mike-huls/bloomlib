import dataclasses
import datetime

import pytest
from bloomlib import BloomFilter
from test.utils.utils_for_testing import random_str, Timer


# todo
# def test_calculate_optimal_n_bits():
#     bloom = BloomSet(expected_number_of_items=1, desired_false_positive_rate=0.05)
#     n_bits:int = bloom.calc_optimal_number_of_bits(expected_number_of_items=10_000, desired_false_pos_rate=0.02168)
#     assert abs(n_bits - 80000) < 300 # should be around 80k

# todo check
# def test_calculate_optimal_n_bits():
#     bloom = BloomSet(expected_number_of_items=1, desired_false_positive_rate=0.05)
#     n_hashes:int = bloom.get_number_of_hashes(bit_array_size=80_000, expected_number_of_items=10_000)
#     assert abs(n_hashes - 5) < 2 # should be around 5

# todo check

def test_can_add_and_contains():

    bloom = BloomFilter(expected_number_of_items=2, desired_false_positive_rate=0.05)
    bloom.add(1)
    assert bloom.contains(item=1)
    assert not bloom.contains(item=1111)

def test_can_add_all_types():

    bloom = BloomFilter(expected_number_of_items=100, desired_false_positive_rate=0.05)

    class Person:
        name:str

        def __init__(self, name:str):
            self.name = name

    @dataclasses.dataclass
    class PersonDataclass:
        name:str

    _string = "string"
    _float = 0.004
    _int = 6546
    _tuple = ("tuple", "of", "strings")
    _list = ["list", "of", "strings"]
    _datetime = datetime.datetime.now()
    _time = datetime.time()
    _class_instance = Person(name="mike")
    _dataclass_instance = PersonDataclass(name="mike")

    bloom.add(_string)
    assert bloom.contains(item=_string)
    assert not bloom.contains(item="not_contained")
    bloom.add(_float)
    assert bloom.contains(item=_float)
    assert not bloom.contains(item=0.04)
    bloom.add(_int)
    assert bloom.contains(item=_int)
    assert not bloom.contains(item=42)
    bloom.add(_tuple)
    assert bloom.contains(item=_tuple)
    assert not bloom.contains(item=('not', 'in'))
    bloom.add(_list)
    assert bloom.contains(item=_list)
    assert not bloom.contains(item=['not', 'in'])
    bloom.add(_datetime)
    assert bloom.contains(item=_datetime)
    assert not bloom.contains(item=datetime.datetime(year=2009, month=2, day=2, hour=1, minute=2, second=3))
    bloom.add(_time)
    assert bloom.contains(item=_time)
    assert not bloom.contains(item=datetime.time(hour=3, minute=3, second=3))
    bloom.add(_class_instance)
    assert bloom.contains(item=_class_instance)
    assert not bloom.contains(item=Person(name="other"))

    # bloom.add(_dataclass_instance)
    # assert bloom.contains(item=_dataclass_instance)
    # assert not bloom.contains(item=PersonDataclass(name="other"))


def test_can_calculate_estimated_fp_rate():
    desired_fp_rate = 0.05
    bloom = BloomFilter(expected_number_of_items=10_000, desired_false_positive_rate=0.05)
    assert bloom.estimate_false_positive_rate() > 0
    assert abs(bloom.estimate_false_positive_rate() - desired_fp_rate) < 0.01   # within 1%

def test_get_correct_fprate_when_adding_ints():
    elem_count = 10_000
    desired_fp_rate = 0.05
    list_of_elements = list(range(elem_count))

    # Create filter and add all elements
    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=desired_fp_rate)
    for i in list_of_elements:
        bloom.add(i)

    # assert all added ints are in the bloom filter
    assert all(bloom.contains(s) for s in list_of_elements)
    # count_observed should fall within a 10% margin around the expected count
    count_expected = elem_count * desired_fp_rate
    count_observed = sum(bloom.contains(i) for i in range(elem_count, elem_count * 2))
    count_observed_wrong_type = sum(bloom.contains(str(i)) for i in range(elem_count, elem_count * 2))
    assert abs(count_expected - count_observed) < count_expected * 0.10
    assert abs(count_expected - count_observed_wrong_type) < count_expected * 0.10

def test_get_correct_fprate_when_bulk_adding_ints():
    elem_count = 10_000
    desired_fp_rate = 0.05
    list_of_elements = list(range(elem_count))

    # Create filter and add all elements
    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=desired_fp_rate)
    bloom.add_bulk(items=list_of_elements)

    # assert all added ints are in the bloom filter
    # assert all(bloom.contains(s) for s in list_of_elements)
    # count_observed should fall within a 10% margin around the expected count
    count_expected = elem_count * desired_fp_rate
    count_observed = sum(bloom.contains(i) for i in range(elem_count, elem_count * 2))
    count_observed_wrong_type = sum(bloom.contains(str(i)) for i in range(elem_count, elem_count * 2))
    assert abs(count_expected - count_observed) < count_expected * 0.10
    assert abs(count_expected - count_observed_wrong_type) < count_expected * 0.10


def test_add_bulk_accepts_all_iterables():
    bloom = BloomFilter(expected_number_of_items=100, desired_false_positive_rate=0.05)

    bloom.add_bulk(items=list([1, 2, 3]))   # list
    bloom.add_bulk(items=tuple([1, 2, 3]))  # tuple
    bloom.add_bulk(items={1, 2, 3})    # set
    with pytest.raises(Exception):
        bloom.add_bulk(items=3)    # int




