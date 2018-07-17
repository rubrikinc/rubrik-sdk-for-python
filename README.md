# Rubrik Cloud Data Management SDK

This project provies a Python package that makes it easy to interfact with the Rubrik CDM API.

The SDK supports Python 2.7, 3.4, 3.5, and 3.6.

## INSTALLATION


Install from source:
```
$ git clone https://github.com/rubrik-devops/rubrik-sdk-for-python
$ cd rubrik-sdk-for-python
$ python setup.py install
```

## USAGE

```python
import rubrik

# Define the Login Credentials
node_ip = "172.21.8.90"
username = "sdk@rangers.lab"
password = "RubrikPythonSDK"

# Connect to the Rubrik Cluster.
rubrik = rubrik.Connect(node_ip, username, password)

# Function Parameters
# api_version: v1 or internal
# api_endpoint: ex. /cluster/me (must begin with `/` and does not include a `/` at the end)
# config (if required): paramter to pass to the API call

# Reponses
# All functions will return the response body documented in the Rubrik API Documentation

# Perform a GET operation against the Rubrik Cluster
# rubrik.get(api_version, api_endpoint) 
rubrik.get('v1', '/cluster/me') 

# Perform a POST operation against the Rubrik Cluster
# rubrik.post(api_version, api_endpoint, config)

config = {
        "hostname": "string",
        "hasAgent": True
    }

rubrik.post('v1' , '/host', config)

# Perform a PATCH operation against the Rubrik Cluster
# rubrik.patch(api_version, api_endpoint, config)

config = {
        "name": "string",
        "timezone": {
            "timezone": "America/Anchorage"
        },
        "geolocation": {
            "address": "string"
        },
        "acceptedEulaVersion": "string"
    }


# Perform a DELETE operation against the Rubrik Cluster
# rubrik.delete(api_version, api_endpoint)
rubrik.delete('v1', '/sla_domain/1a98504e-ppd1-411d-e235-814dc045ab87')

# Monitor the status of a Rubrik Job (ex. on-demand snapshot)
# rubrik.job_status(url) (job status url found through a relevant POST command)
url = "https://172.21.8.90/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_1f51a68c-6fe1448-vm-5008_ecd2-4765-49fa-81f2-19ba417:::0"
rubrik.job_status(url)
```

Example PATCH call in the Rubrik API Explorer

![Example PATCH API call in the Rubrik API Explorer](https://user-images.githubusercontent.com/8610203/42196675-dafd8130-7e44-11e8-968e-4896ac0e4b2c.png)

## AUTHOR INFORMATION

<p></p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/8610203/37415009-6f9cf416-2778-11e8-8b56-052a8e41c3c8.png" alt="Rubrik Ranger Logo"/>
</p>