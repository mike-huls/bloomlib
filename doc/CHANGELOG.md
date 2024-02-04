# Changelog
All notable changes to this project will be documented in this file.
 - `Added` for new features.
 - `Changed` for changes in existing functionality.
 - `Deprecated` for soon-to-be removed features.
 - `Removed` for now removed features.
 - `Fixed` for any bug fixes.
 - `Security` in case of vulnerabilities.
<hr>
 

## Upcoming features
- fix nhashes changed due to bitvec
- make bloomfilter serializable and deserializable 
- Make class instances and dataclass instances hashable in pywrapper
- Benchmark agains `pybloom`, `bloomfilter3` and `bloomfilter`
<hr>

## 2022-02-03 - v0.0.2
### Optimizations and fixes 
#### Added
- pywrapper: `add_bulk` method on BloomFilter now accepts any Iterable instead of just a list
#### Changed
- BloomFilter now uses array of bits instead of Vec<u8>
- Made bitarray and hashes private; added get methods



## 2022-01-30 - v0.0.1
### Release version 0.0.1
Released

## 2022-01-30 - v0.0.0
### Initial release 
