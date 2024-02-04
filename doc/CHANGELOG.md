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
- make bloomfilter serializable and deserializable 
- Benchmark agains `pybloom`, `bloomfilter3` and `bloomfilter`
<hr>

## 2022-02-04 - v0.0.2
### Optimizations and fixes 
#### Added
- pywrapper: `add_bulk` method on BloomFilter now accepts any Iterable instead of just a list
- add methods for getting bits (memory) and number of hashes
#### Changed
- BloomFilter now uses array of bits instead of Vec<u8>
- Made bitarray and hashes private; added get methods
### Fixed
- pywrapper: `add_bulk` better parsing
- now accepts class-instances (hashing)


## 2022-01-30 - v0.0.1
### Release version 0.0.1
Released

## 2022-01-30 - v0.0.0
### Initial release 
