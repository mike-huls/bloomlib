import time

from bloomset_rs import BloomSet


def test_demo():
    LENGTH = 10_000

    bs = BloomSet(expected_number_of_items=LENGTH, desired_false_positive_rate=0.005)

    print(bs.get_number_of_hashes())
    print(bs.get_number_of_bits())
    quit()

    the_list = list(range(LENGTH))
    strt = time.perf_counter()
    bs.add_bulk(the_list)
    print(f"added {LENGTH} in {time.perf_counter() - strt}")
    print("current number of hashes", bs.get_number_of_hashes())
    print("current number of bits", bs.get_number_of_bits())

    print(bs.contains(1))
    print(bs.contains(100))
    print(bs.contains(1000000))


if __name__ == "__main__":
    test_demo()