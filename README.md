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
* [BLOG: Hello World! Welcoming Rubrik’s Python SDK](https://www.rubrik.com/blog/introducing-rubrik-python-sdk/)
