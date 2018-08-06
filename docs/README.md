# Rubrik SDK for Python

## Installation

Install from source:
```
$ git clone https://github.com/rubrik-devops/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
``` 

## Configuration

Before you begin to use the Rubrik Python SDK, you should first setup your autentication credentials. By default, the SDK will attempt to read the the Rubrik Cluster credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`

## Usage

To use the SDK, you must first instantiate a new variable, in thise case `rubrik`, to connect to the Rubrik Cluster.

```py
import rubrik
rubrik = rubrik.Connect()
```

{% hint style="info" %}
Note: You may use any variable name to connect to the Rubrik Cluster.
{% endhint %}

If you have not configured the correct environment variables you may also manually pass in the required authentication credentials.

```py
import rubrik

node_ip = "172.21.8.90"
username = "sdk@rangers.lab"
password = "RubrikPythonSDK"

rubrik = rubrik.Connect(node_ip, username, password)
```