from typing import List, Any

class BloomFilter:
    """
    A class representing a bloom filter that you can use as a set

    :param expected_number_of_items: the number of items you expect to store; used to optimize the filter size
    :param desired_false_positive_rate: the percentage of false positives you accept expressed as a float between 0 and 1
    """
    def __init__(self, expected_number_of_items: int, desired_false_positive_rate: float) -> None: ...
    def add(self, values: Any) -> None:
        """
        Adds a value to the bloomset
    
        :param values: List of values that you want added to the bloomset
        :return: void
        """
    def add_bulk(self, items: List[Any]) -> None:
        """
        Add items in bulk to the Bloom Filter
        :param items: List of items
        :return: void
        """
    def contains(self, item: Any) -> bool:
        """
        Looks up whether an item is
        :param item: lookup if the Bloom filter contains this item
        :return: bool representing that the item is definitely not contained (false) or maybe (true)
        """

    def get_number_of_hashes(self) -> int:
        """
        Returns the number of hash functions this BloomFilter uses
        :return: int representing the number of hashes this Bloom filter uses
        """
    def get_number_of_bits(self) -> int:
        """
        Memory size
        :return: int representing the number of bits that the Bloom filter's memory uses
        """