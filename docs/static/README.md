# Rubrik SDK for Python

## Introduction to the Rubrik SDK for Python

Rubrik’s API first architecture enables organizations to embrace and integrate Rubrik functionality into their existing automation processes. While Rubrik APIs can be consumed natively, companies are at various stages in their automation journey with different levels of automation knowledge on staff. The Rubrik Software Development Kit (SDK) for Python extends upon Python’s easy to understand programming language, transforming Rubrik functionality into easy to consume functions. This eliminates the need to understand how to consume raw Rubrik APIs with Python and extends upon one of Rubrik’s main design centers - simplicity.

## Installation

The SDK has been tested against Python 2.7.6 and Python 3.6.4.

Install from pip:

`pip install rubrik_cdm`

Install from source:
```
$ git clone https://github.com/rubrikinc/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
``` 

## Configuration

Before you begin to use the Rubrik Python SDK, you should first setup your authentication credentials. By default, the SDK will attempt to read the the Rubrik Cluster & Polaris credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`
* `rubrik_cdm_token`
* `rubrik_polaris_domain`
* `rubrik_polaris_username`
* `rubrik_polaris_password`

| Note: The `rubrik_cdm_username` and `rubrik_cdm_password` must be supplied together and may not be provided if the `rubrik_cdm_token` variable is present|

## Getting Started

The SDK contains two separate modules, one for interacting with CDM and the other for Polaris. Choose a module-specific guide below:

* [rubrik_cdm](rubrik_cdm/getting_started.md)
* [rubrik_polaris](rubrik_polaris/getting_started.md)
