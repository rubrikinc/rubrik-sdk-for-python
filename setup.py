#! /usr/bin/env python

import setuptools

long_description = """
# Rubrik SDK for Python

This project provides a Python package that makes it easy to interact with the Rubrik CDM API.

The SDK has been tested against Python 2.7.6 and Python 3.6.4.

## Installation

Install from pip:

`pip install rubrik_cdm`

Install from source:
```
$ git clone https://github.com/rubrik-devops/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
```
## Quick Start

* [Quick Start Guide](https://github.com/rubrikinc/rubrik-sdk-for-python/blob/master/docs/quick-start.md)

## Documentation

* [SDK Documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python/)
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)

## Example

By default, the Rubrik SDK will attempt to read the the Rubrik Cluster credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()
```

## Additional Links
* [VIDEO: Getting Start with the Rubrik SDK for Python](https://www.youtube.com/watch?v=TQM60X2_r_c&feature=youtu.be)
"""


setuptools.setup(
    name="rubrik_cdm",
    version="2.0.1",
    author="Rubrik Build",
    description="A Python package for interacting with the Rubrik CDM API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rubrik-devops/rubrik-sdk-for-python",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6"
    ],
    install_requires=[
        'requests >= 2.18.4',
        'python-dateutil',
        'pytz'
    ],
    tests_require=[
        'pytest'
    ],
    zip_safe=True,
)
