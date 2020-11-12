# Rubrik Polaris SDK - Quick Start Guide

## Authentication Mechanisms

The Rubrik SDK for Python provides two mechanisms for supplying credentials to the `rubrik_polaris.PolarisClient()` function. Credentials may be accessed through the use of environment variables or manually passed into the function as parameters.

### Authenticating with Environment Variables

Storing credentials in environment variables is a more secure process than directly hard coding them into scripts and ensures that your credentials are not accidentally shared if your code is uploaded to an internal or public version control system such as GitHub. If no arguments are passed to the `rubrik_polaris.PolarisClient()` function, it will attempt to read the Rubrik Polaris credentials from the following environment variables:

* **`rubrik_polaris_domain`** (Contains the customer domain name, the first part of the URL given to you, https://<domain>.my.rubrik.com)
* **`rubrik_polaris_username`** (Contains a username with configured access to Polaris)
* **`rubrik_polaris_password`** (Contains the password for the above user)

The way in which to populate these environment variables differs depending on the operating system running Python. Below are examples for Windows, Linux, and Mac OS.

Once set, the `rubrik_polaris.PolarisClient()` function will automatically utilize the data within the environment variables to perform its connection unless credentials are specifically passed in the arguments of the function.

### Authenticate by Providing Username and Password

Although the use of environment variables are recommended, there may be scenarios where directly sending credentials to the `rubrik_polaris.PolarisClient()` function as parameters makes sense. When arguments are provided, any environment variable information, populated or unpopulated, is ignored. To pass connection and credential information, simply call the `rubrik_polaris.PolarisClient()` function, passing the node IP, username, and password as follows:

```py
domain = "example"
username = "jane.doe@example.com"
password = "s3cr3tP_a55w0R)"

client = rubrik_polaris.PolarisClient(domain, username, password)
```

Mixing the usage of both environment and hard coded variables is supported. The below example is run under the pretense that the `rubrik_polaris_username` and `rubrik_polaris_username` environment variables have been set, providing only the password to the connect function.

`client = rubrik_polaris.PolarisClient(password="s3cr3tP_a55w0R)")`


## Connecting to Rubrik Polaris

The Rubrik SDK for Python utilizes the `rubrik_polaris.PolarisClient()` function to construct a client connected to Polaris using the provided credentials. `rubrik_polaris.PolarisClient()` only needs to be called once, assigning the response to a variable to be used for subsequent calls throughout the remainder of the Python session. To initiate the function, first import the `rubrik_polaris` module and assign the response of `rubrik_polaris.PolarisClient()` to a variable as follows:

```py
from rubrik_polaris import PolarisClient

client = PolarisClient()
```

Any subsequent calls to methods or functions within the `rubrik_polaris` module are now executed through the context of the variable used to store the response from the `PolarisClient()` method. For example, to retrieve the all the SLA Domains defined in your account, use:

```py
from rubrik_polaris import PolarisClient

client = PolarisClient()
print(client.get_sla_domains())
```

For a full list of functions, methods, and their associated arguments see the official [Rubrik SDK for Python documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python).

### Certificate Validation

When connecting to a Rubrik cluster without certificate validation enabled you will receive the following warning message:

```
/usr/local/lib/python3.6/site-packages/urllib3/connectionpool.py:857: 
InsecureRequestWarning:
Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
See: 
https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warningsInsecureRequestWarning)
```

This warning may be suppressed utilizing the `urllib3` library and inserting the following code within your script:

```py
from rubrik_polaris import PolarisClient
import urllib3

urllib3.disable_warnings()

client = PolarisClient()
```


