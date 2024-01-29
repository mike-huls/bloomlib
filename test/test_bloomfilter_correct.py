import dataclasses
import datetime

from bloomlib import BloomFilter, estimate_false_positive_rate
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
def test_calculate_estimated_fp_rate():
    # bloom = BloomFilter(expected_number_of_items=1, desired_false_positive_rate=0.05)
    # estimated_fp_rate:float = estimate_false_positive_rate(n_hashes=5, mem_size=80_000, n_items=10_000)
    estimated_fp_rate = estimate_false_positive_rate(50_000, 80_000, 10_000)
    print('----', estimated_fp_rate)
    assert estimated_fp_rate != 0

    assert abs(estimated_fp_rate - 0.0216) < 0.01 # should be around 0.0216

def test_one_thing():

    bloom = BloomFilter(expected_number_of_items=2, desired_false_positive_rate=0.05)
    bloom.add(1)

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

def test_false_positive_rate():

    elem_count = 10_000

    bloom = BloomFilter(expected_number_of_items=elem_count, desired_false_positive_rate=0.05)

    with Timer("Making strs"):
        strs = {random_str(16) for _ in range(elem_count)}

    with Timer("Adding strs"):
        for s in strs:
            bloom.add(s)

    with Timer("checking no false negatives"):
        assert all(bloom.contains(s) for s in strs)

    with Timer("checking false positives"):
        false_positives = sum(bloom.contains(random_str(15)) for _ in range(elem_count))

    fpr_estimated = estimate_false_positive_rate(bloom.get_number_of_hashes(), bloom.get_number_of_bits(), elem_count)
    print(f"False positive estimate: {fpr_estimated * 100:.05f}%")


    fpr_empirical = false_positives / elem_count
    print(f"False positives: {false_positives} ({fpr_empirical * 100:.05f}%)")

# todo
# def test_serialize_deserialize():
#     bloom = BloomSet(expected_number_of_items=100, desired_false_positive_rate=0.05)
#     bloom.add_bulk(items=list(range(100)))
#     print(bloom.to_dict())




