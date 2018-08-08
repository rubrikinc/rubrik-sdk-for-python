# Rubrik SDK for Python

## Installation

The SDK supports Python 2.7, 3.4, 3.5, and 3.6.

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

When connecting to the Rubrik Cluster for the first time, the SDK will use `cluster_node_ip()` to retrieve a list of the management IP address for each node in the Cluster. As a best practice, the SDK will randomly choose a IP from that list for all subsequent API calls.

## Debug

To enable debuging set the `Connect()` `enable_logging` keyword argument to `True`.

### Example

Script:

```py
import rubrik
rubrik = rubrik.Connect(enable_logging=True)

cluster_version = rubrik.cluster_version()
print(cluster_version)
```

Output:

```
[2018-08-08 09:18:59,687] [DEBUG] -- User Provided Node IP: 172.21.8.53
[2018-08-08 09:18:59,687] [DEBUG] -- Username: demo
[2018-08-08 09:18:59,687] [DEBUG] -- Password: *******

[2018-08-08 09:18:59,687] [DEBUG] -- cluster_node_ip: Generating a list of all Cluster Node IPs.
[2018-08-08 09:18:59,687] [DEBUG] -- GET https://172.21.8.53/api/internal/cluster/me/node
[2018-08-08 09:19:00,062] [DEBUG] -- <Response [200]>

[2018-08-08 09:19:00,062] [DEBUG] -- cluster_version: Getting the software version of the Rubrik Cluster.
[2018-08-08 09:19:00,062] [DEBUG] -- GET https://172.21.8.54/api/v1/cluster/me/version
[2018-08-08 09:19:00,443] [DEBUG] -- <Response [200]>

{'version': '4.1.2-2366'}
```

