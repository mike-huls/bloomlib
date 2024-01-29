import hashlib
import random
import string
from dataclasses import dataclass
import time
from typing import Callable


@dataclass
class Timer:
    msg: str
    start: float = 0.0
    end: float = 0.0

    def __enter__(self):
        print(self.msg, end=": ")
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        print(f"{self.end - self.start:.02f}s")




nice_chars = string.printable

def random_str(length: int) -> str:
    return ''.join(random.choices(nice_chars, k=length))

# def bitarray_example():
#     bits = BitArray.from_iterable([1, 1, 0, 1, 1, 1, 0, 1])
#     print(len(bits))
#     # bits[0] = 0
#     print(bits)
#     print(BitArray.zeros(2))

def split_long_hash(
        hash_fn: Callable,
        digest_size: int,
        hashes: int,
        bytes_per_hash: int,
) -> Callable:
    if digest_size // hashes < bytes_per_hash:
        raise ValueError("digest not long enough")

    def calc_hashes(item):
        item_hash = hash_fn(item)
        hash_bytes = item_hash.to_bytes(digest_size, byteorder='big')
        return [
            int.from_bytes(hash_bytes[i * bytes_per_hash:(i + 1) * bytes_per_hash], byteorder='big')
            for i in range(hashes)
        ]

    return calc_hashes


def long_hash(s: str) -> int:
    h = hashlib.sha256()
    h.update(s.encode())
    return int.from_bytes(h.digest(), byteorder='big')  # Specify 'big' or 'little' based on your requirement
