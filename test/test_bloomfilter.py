import dataclasses
import datetime

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

    @dataclasses.dataclass
    class Person:
        name:str

    _string = "string"
    _float = 0.004
    _int = 6546
    _immutable_col = ("tuple", "of", "strings")
    _mutable_col = ["list", "of", "strings"]
    _datetime = datetime.datetime.now()
    _time = datetime.time()
    _dataclass = Person(name="mike")

    bloom.add(_string)
    bloom.add(_float)
    bloom.add(_int)
    bloom.add(_immutable_col)
    bloom.add(_mutable_col)
    bloom.add(_datetime)
    bloom.add(_time)
    # bloom.add(_dataclass)


def test_can_calculate_estimated_fp_rate():
    desired_fp_rate = 0.05
    bloom = BloomFilter(expected_number_of_items=10_000, desired_false_positive_rate=0.05)
    assert bloom.estimate_false_positive_rate() > 0
    assert abs(bloom.estimate_false_positive_rate() - desired_fp_rate) < 0.01   # within 1%

def test_false_positive_rate():

    elem_count = 10_000
    desired_fp_rate = 0.05

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=desired_fp_rate)

    # Generate strings and add to bloom filter
    strs = {str(i) for i in range(elem_count)}
    bloom.add_bulk(items=list(strs))

    # assert all added strings are in the bloom filter
    assert all(bloom.contains(s) for s in strs)
    false_positives = sum(bloom.contains(str(i)) for i in range(elem_count, elem_count * 2))

    # Compare calculated fp-rate with observed
    fpr_estimated = bloom.estimate_false_positive_rate()
    print(f"False positive estimate: {fpr_estimated * 100:.05f}%")
    fpr_empirical = false_positives / elem_count
    print(f"False positives: {false_positives} ({fpr_empirical * 100:.05f}%)")





