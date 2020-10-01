# Rubrik SDK for Python

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

Before you begin to use the Rubrik Python SDK, you should first setup your authentication credentials. By default, the SDK will attempt to read the the Rubrik Cluster credentials from the following environment variables:

* `rubrik_cdm_node_ip`
* `rubrik_cdm_username`
* `rubrik_cdm_password`
* `rubrik_cdm_token`

| Note: The `rubrik_cdm_username` and `rubrik_cdm_password` must be supplied together and may not be provided if the `rubrik_cdm_token` variable is present|
| --- |

## Usage

To use the SDK, you must first instantiate a new variable, in thise case `rubrik`, to connect to the Rubrik Cluster.

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()
```

{% hint style="info" %}
Note: You may use any variable name to connect to the Rubrik Cluster.
{% endhint %}

If you have not configured the correct environment variables you may also manually pass in the required authentication credentials.

```py
import rubrik_cdm

node_ip = "172.21.8.90"
username = "sdk@rangers.lab"
password = "RubrikPythonSDK"

rubrik = rubrik_cdm.Connect(node_ip, username, password)
```

```py
import rubrik_cdm

node_ip = "172.21.8.90"
api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUVkN2FhYzlfZWU0MzA5ODQtMGE1Zi00NGZjLTliNTYtN"

rubrik = rubrik_cdm.Connect(node_ip, api_token=api_token)
```


## Logging

To enable logging, set the `Connect()` `enable_logging` keyword argument to `True`.

The `logging_level` argument can then be used to set the specific logging level you wish to use. The following levels are valid choices:

* `debug` (default value)
* `critical` 
* `error` 
* `warning` 
* `info`

### Example

Script:

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect(enable_logging=True, logging_level="info)

cluster_version = rubrik.cluster_version()
print(cluster_version)
```

Output:

```
[2018-08-08 09:18:59,687] [INFO] -- Node IP: 172.21.8.53
[2018-08-08 09:18:59,687] [INFO] -- Username: demo
[2018-08-08 09:18:59,687] [INFO] -- Password: *******

[2018-08-08 09:19:00,062] [INFO] -- cluster_version: Getting the software version of the Rubrik Cluster.
[2018-08-08 09:19:00,062] [INFO] -- GET https://172.21.8.54/api/v1/cluster/me/version
[2018-08-08 09:19:00,443] [INFO] -- <Response [200]>

4.1.2-2366
```

## Certificate Verification

When connecting to a Rubrik cluster without certificate verification enabled (see the Rubrik CDM Security Guide for additional information) you will receive the following warning message:

```
/usr/local/lib/python3.6/site-packages/urllib3/connectionpool.py:857: InsecureRequestWarning: 
Unverified HTTPS request is being made. Adding certificate verification is strongly advised. 
See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warningsInsecureRequestWarning)
```

To supress this warning add the following code to your script:

```py
import urllib3
urllib3.disable_warnings()
```
