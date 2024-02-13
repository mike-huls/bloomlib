[//]: # (<div align="center">)
[//]: # (  <img src="https://pandas.pydata.org/static/img/pandas.svg"><br>)
[//]: # (</div>)

```commandline
______  ______                          ___________ ______  
___  /_ ___  /______ ______ _______ ___ ___  /___(_)___  /_ 
__  __ \__  / _  __ \_  __ \__  __ `__ \__  / __  / __  __ \
_  /_/ /_  /  / /_/ // /_/ /_  / / / / /_  /  _  /  _  /_/ /
/_.___/ /_/   \____/ \____/ /_/ /_/ /_/ /_/   /_/   /_.___/ 
```
-----------------

# bloomlib: superfast Bloom filters for Python, optimized in Rust

|         |                                                                                                                                                                                                                                      |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Package | [![PyPI Latest Release](https://img.shields.io/pypi/v/bloomlib.svg)](https://pypi.org/project/bloomlib/) [![PyPI Downloads](https://img.shields.io/pypi/dm/bloomlib.svg?label=PyPI%20downloads)](https://pypistats.org/packages/bloomlib) |
| Meta    | ![GitHub License](https://img.shields.io/github/license/mike-huls/bloomlib)                                                                                                                                                          |

**bloomlib** is a Python package that provides superfast Bloom filters, designed to 
optimize your applications in an easy and intuitive way.
It aims to be the go-to package to build and use Bloom Filters that make your applications 
superfast, memory-efficient and user-friendly.
```shell
pip install bloomlib
```

## Table of Contents
- [Main Features](#main-features)
- [Usage Example](#usage-example)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [License](#license)
- [Documentation](#documentation)
- [Development](#development)
- [Contributing to bloomlib](#contributing-to-bloomlib)

## Main Features
- 🦀 Built in Rust
- ⚡ Highly optimized for speed and memory-efficiency
- 👨‍🎨 User-friendly

## Usage Example
```python
from bloomlib import BloomFilter

# 1. Create the filter
bf = BloomFilter(expected_number_of_items=1_000, desired_false_positive_rate=0.05)

# 2. Add items
for i in range(100):
    bf.add(item=i)

# 3. Check if an item is contained; False means definitely not, True means "maybe" 
if (bf.contains(item=42)):
    print("This item may be in filter")
else:
    print("This item is definitely not in the filter")
```


## Installation
```sh
pip install bloomlib
```
The source code is currently hosted on GitHub at:
https://github.com/mike-huls/bloomlib

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/bloomlib).

## Dependencies
Bloomlib has no Python dependencies

## License
[MIT](LICENSE.txt)

## Documentation
🔨 Under construction

## Development
Find the changelog and list of upcoming features [here](doc/CHANGELOG.md).
<br>
**Contributions** are always welcome; feel free to submit bug reports, bug fixes, feature requests, documentation improvements or enhancements!

<hr>

[Go to Top](#table-of-contents)