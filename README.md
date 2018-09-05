# Rubrik Cloud Data Management SDK for Python

This project provies a Python package that makes it easy to interact with the Rubrik CDM API.

The SDK has been tested against Python 2.7.6 and Python 3.6.4.

**[Full Documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python/)**


## INSTALLATION

Install from pip:

`pip install rubrik_cdm`

Install from source:
```
$ git clone https://github.com/rubrik-devops/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
```

## Quick Start


By default, the Rubrik SDK will attempt to read the the Rubrik Cluster credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()
```

## AUTHOR INFORMATION

<p></p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/8610203/37415009-6f9cf416-2778-11e8-8b56-052a8e41c3c8.png" alt="Rubrik Ranger Logo"/>
</p>