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

{% hint style="info" %}
Note: The following assumes that the Rubrik cluster has already been boostraped. If that has not been completed yet see the `Bootstrapping the Rubrik cluster` section below.
{% endhint %}

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


## Bootstrapping the Rubrik cluster

### Arguments
| Name                   | Type | Description                                                                    |
|------------------------|------|--------------------------------------------------------------------------------|
| node_ip                | str  | The node IP address of a node in the Rubrik cluster.                           |
| cluster_name           | str  | Unique name to assign to the Rubrik cluster.                                   |
| admin_email            | str  | The Rubrik cluster sends messages for the admin account to this email address. |
| admin_password         | str  | Password for the admin account.                                                |
| management_gateway     | str  | IP address assigned to the management network gateway                          |
| management_subnet_mask | str  | Subnet mask assigned to the management network.                                |

### Keyword Arguments
| Name                | Type | Description                                                                                                  | Default        |
|---------------------|------|--------------------------------------------------------------------------------------------------------------|----------------|
| enable_encryption   | bool | Enable software data encryption at rest.                                                                     | True           |
| node_config         | dict | The Node Name and IP formatted as a dictionary.                                                              | None           |
| dns_search_domains  | str  | The search domain that the DNS Service will use to resolve hostnames that are not fully qualified.           | None           |
| dns_nameservers     | list | IPv4 addresses of DNS servers.                                                                               | [8.8.8.8]      |
| ntp_servers         | list | FQDN or IPv4 address of a network time protocol (NTP) server.                                                | [pool.ntp.org] |
| wait_for_completion | bool | Flag to determine if the function should wait for the Bootstrap process to finish.                           | True           |
| timeout             | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. | 15             |

## Returns
| Type | Return Value                                                    |
|------|-----------------------------------------------------------------|
| dict | The response returned by `POST /internal/cluster/me/bootstrap`. |

### Example


```py
# Example Cloud Cluster Bootstrap

import rubrik

enable_encryption = False # Encryption should only be set to False when bootstrapping a Cloud Cluster
node_ip = '172.26.7.199'
node_config = {
    '1': node_ip,
    '2': '172.26.7.200',
    '3': '172.26.7.201',
    '4': '172.26.7.201'
}

cluster_name = 'Python-SDK'
admin_email = 'pythonsdk@example.com'
admin_password = 'RubrikGoForward'
management_gateway = '172.26.7.1'
management_subnet_mask = '255.255.255.0'


bootstrap = rubrik.Bootstrap(node_ip, cluster_name, admin_email, admin_password, management_gateway, management_subnet_mask, node_config, enable_encryption=enable_encryption, wait_for_completion=True enable_logging=True)
```

{% hint style="info" %}
Note: You may use any variable name to connect to the Rubrik Cluster.
{% endhint %}