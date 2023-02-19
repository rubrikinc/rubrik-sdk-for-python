# Quick Start Guide: Rubrik SDK for Python

## Introduction to the Rubrik SDK for Python

Rubrik’s API first architecture enables organizations to embrace and integrate Rubrik functionality into their existing automation processes. While Rubrik APIs can be consumed natively, companies are at various stages in their automation journey with different levels of automation knowledge on staff. The Rubrik Software Development Kit (SDK) for Python extends upon Python’s easy to understand programming language, transforming Rubrik functionality into easy to consume functions. This eliminates the need to understand how to consume raw Rubrik APIs with Python and extends upon one of Rubrik’s main design centers - simplicity.

## Authentication Mechanisms

The Rubrik SDK for Python provides two mechanisms for supplying credentials to the `rubrik_cdm.Connect()` function. Credentials may be accessed through the use of environment variables or manually passed into the function as parameters.

### Authenticating with Environment Variables

Storing credentials in environment variables is a more secure process than directly hard coding them into scripts and ensures that your credentials are not accidentally shared if your code is uploaded to an internal or public version control system such as GitHub. If no arguments are passed to the `rubrik_cdm.Connect()` function, it will attempt to read the Rubrik Cluster credentials from the following environment variables:

* **`rubrik_cdm_node_ip`** (Contains the IP/FQDN of a Rubrik node)
* **`rubrik_cdm_username`** (Contains a username with configured access to the Rubrik cluster)
* **`rubrik_cdm_password`** (Contains the password for the above user)
* **`rubrik_cdm_token`** (Contains the the API token used for authentication)

| Note: The `rubrik_cdm_username` and `rubrik_cdm_password` must be supplied together and may not be provided if the `rubrik_cdm_token` variable is present|
| --- |

The way in which to populate these environment variables differs depending on the operating system running Python. Below are examples for Windows, Linux, and Mac OS.

#### Setting Environment Variables in Microsoft Windows

For Microsoft Windows-based operating systems the environment variables can be set utilizing the `setx` command as follows:

```
setx rubrik_cdm_node_ip "192.168.0.100"
setx rubrik_cdm_username "user@domain.com"
setx rubrik_cdm_password "SecretPassword"
setx rubrik_cdm_token "CDMToken"
```

#### Setting Environment Variables in macOS and \*nix

For macOS and \*nix based operating systems the environment variables can be set utilizing the export command as follows:

```
export rubrik_cdm_node_ip=192.168.0.100
export rubrik_cdm_username=user@domain.com
export rubrik_cdm_password=SecretPassword
export rubrik_cdm_token=CDMToken
```

In order for the environment variables to persist across terminal sessions, add the above three export commands to the `~\.bash_profile` or ~\.profile file and then run `source ~\.bash_profile` or `source ~\.profile` to ensure the environment variables are present in your current terminal session.

Once set, the `rubrik_cdm.Connect()` function will automatically utilize the data within the environment variables to perform its connection unless credentials are specifically passed in the arguments of the function.

### Authenticate by Providing Username and Password or API Token

Although the use of environment variables are recommended, there may be scenarios where directly sending credentials to the `rubrik_cdm.Connect()` function as parameters makes sense. When arguments are provided, any environment variable information, populated or unpopulated, is ignored. To pass connection and credential information, simply call the `rubrik_cdm.connect()` function, passing the node IP, username, and password as follows:

```python
node_ip = "192.168.0.100"
username = "user@domain.com"
password = "SecretPassword"

rubrik = rubrik_cdm.Connect(node_ip, username, password)
```

Or by passing the node IP and API Token as follows:

```python
node_ip = "192.168.0.100"
api_token = "jf2jma02k3anms0"

rubrik = rubrik_cdm.Connect(node_ip, api_token=api_token)
```


Mixing the usage of both environment and hard coded variables is supported. The below example is run under the pretense that the `rubrik_cdm_node_ip` and `rubrik_cdm_password` environment variables have been set, providing only the password to the connect function.

`rubrik = rubrik_cdm.Connect(password="SecretPassword")`


## Connecting to a Rubrik Cluster

The Rubrik SDK for Python utilizes the `rubrik_cdm.Connect()`function as a mechanism to provide credentials to  Rubrik CDM. `rubrik_cdm.Connect()` only needs to be called once, assigning the response to a variable to be used for subsequent calls throughout the remainder of the Python session. To initiate the function, first import the `rubrik_cdm` package and assign the response of `rubrik_cdm.Connect()` to a variable as follows:

```python
import rubrik_cdm
rubrik = rubrik_cdm.Connect()
```

| Note: You may use any variable name to connect to the Rubrik cluster. |
| --- |

Any subsequent calls to methods or functions within the rubrik_cdm package are now executed through the context of the variable used to store the response from the Connect() method. For example, to retrieve the VMware VMs within the Gold SLA Domain the following code is used:

```python
import rubrik_cdm
rubrik = rubrik_cdm.Connect()
print rubrik.get_sla_objects("Gold","VMware")
```

For a full list of functions, methods, and their associated arguments see the official [Rubrik SDK for Python documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python).

### Certificate Validation

Certificate validation can be turned on by setting verify=True when connecting the cluster:

````
import rubrik_cmd
rubrik = rubrik_cdm.Connect(verify=True)
```

When connecting to a Rubrik cluster without certificate validation enabled you will receive the following warning message:

```
/usr/local/lib/python3.6/site-packages/urllib3/connectionpool.py:857: 
InsecureRequestWarning:
Unverified HTTPS request is being made. Adding certificate verification is strongly advised.
See: 
https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warningsInsecureRequestWarning)
```

This warning may be suppressed utilizing the `urllib3` library and inserting the following code within your script:

```python
import rubrik_cdm
import urllib3

urllib3.disable_warnings()

rubrik = rubrik_cdm.Connect()
```

| Note: It is strongly advised that valid certificates are installed and utilized on the Rubrik cluster. For more information see the [Rubrik CDM Security Guide](https://support.rubrik.com/servlet/servlet.FileDownload?file=00P1W00001EQnaYUAT). |
| --- |

## Rubrik SDK for Python Quick Start

The following section outlines how to get started using the Rubrik SDK for Python, including installation, configuration, as well as sample code.

### Prerequisites

The following are the prerequisites in order to successfully install and run the sample code included in this quickstart guide:

* Python (Tested against v2.7.6 and v3.7.4)
* The [pip package management tool](https://pip.pypa.io/en/stable/)
* Rubrik CDM

### Installation

The Rubrik SDK for Python can be installed into a Python environment either by utilizing the pip package manager or installing from source.

|Note: Installing from source should only be used when performing development work on the Rubrik SDK for Python or if the environment does not allow for pip installations. The easiest and most common way to install the Rubrik SDK for Python is through the pip package manager. |
| --- |

#### Install using the pip package manager

Due to the popular uptake of the pip package manager Rubrik also maintains a copy of the Rubrik SDK for Python hosted within the Python Package Index. This allows for developers and operations to install the Rubrik SDK for Python using pip as follows.

```
pip install rubrik-cdm
```

The pip installation method will take care of downloading and installing all dependencies of the Rubrik SDK for Python. 

#### Install from Source

As the Rubrik SDK for Python is hosted on GitHub, installing from source allows for the added benefit of being able to access newly created and “beta” type features as they are developed and pushed to the repository. 

To install the Rubrik SDK for Python from source run the following commands.

```
git clone https://github.com/rubrikinc/rubrik-sdk-for-python
cd rubrik-sdk-for-python
sudo python setup.py install
```

|Note: After executing `setup.py` install, all dependencies will be automatically downloaded and installed. |
| --- |

### Sample Syntax - VMware Virtual Machine Operations

The following code will walk through a number of real-world examples of protecting and restoring VMware Virtual Machines. For a complete listing of available functionality see the complete [Rubrik SDK for Python documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python).

#### Setting up the Sample Workflow

Create a file named `vmwarevms.py` in your working directory and copy in the following code:

```python
import rubrik_cdm
import urllib3

# Disable certificate warnings and connect to Rubrik Cluster
urllib3.disable_warnings()

# Establish a connection to the Rubrik cluster
rubrik=rubrik_cdm.Connect()

#=============================================================
# Example of protecting a VMware Virtual Machine
#=============================================================

# Set Object Variables
vm_name = "VM1"
sla_name = "Gold"
object_type = "VMware"

# Assign VM to SLA Domain
assign_sla = rubrik.assign_sla(vm_name, sla_name, object_type)

#=============================================================
# Example of taking an On-Demand Snapshot of a VMware VM
#=============================================================

# Set Object Variables
vm_name = "VM1"
sla_name = "Gold"
object_type = "VMware"

# Take On-Demand Snapshot of VM
snapshot = rubrik.on_demand_snapshot(vm_name, object_type, sla_name)

#=============================================================
# Recovering VMware Virtual Machines
#=============================================================

# Set Object Variables

vm_name = "VM1"
date = "10-21-2018"
time = "9:56 AM"

# Live Mount specific snapshot to the current host
live_mount = rubrik.vsphere_live_mount(vm_name, date, time)

# Live Mount latest snapshot to a specific host
live_mount = rubrik.vsphere_live_mount(vm_name, date='latest', time='latest', host='esxi44.rubrik.us')

# Instant Recovery of the latest snapshot to the current host
instant_recovery = rubrik.vsphere_instant_recovery(vm_name, date='latest', time='latest')

```

#### Breaking Down the Sample Workflow

After importing the needed modules, disabling certificate warnings and connecting to the Rubrik cluster, the main examples start on Line 8. 

**Lines 8 through 18** show an example of associating an existing SLA Domain with a VMware VM. The `assign_sla(`) function is utilized to accomplish this, taking in three arguments; the VM name, SLA Domain name, and Object Type (VMware).

**Lines 20 through 30** illustrate performing an on-demand snapshot of a VMware VM. The `on_demand_snapshot()` function is utilized to accomplish this, taking in three arguments; the VM name, object type (VMware), and SLA Domain name to apply to the snapshot. The SLA Domain name is an optional requirement and if not specified the currently associated SLA Domain of the VM will be used.

**Lines 32 through 49** illustrate a couple of different recovery options for VMware VMs. The first, on Line 42 is a Live Mount of a specific snapshot to the same host which is running the production VM. Line 46 shows a Live Mount of the same VM, only utilizing the most recent snapshot and specifying a host on which to mount the VM. Line 49 performs an Instant Recovery of the VM utilizing the most recent available snapshot.

|Note: the `vpshere_live_mount()` and `vsphere_instant_recovery()`functions support many more arguments and options which are utilized in this sample. For the complete list of functionality available for managing VMware VMs see the Rubrik SDK for Python documentation. |
| --- |

#### Running the Sample Workflow

Once `vmwarevms.py` is saved within the working directory execute the code with the following statement:

```
python vmwarevms.py
```

### Sample Syntax - Physical Host Operations

The following code will walk through a number of real-world examples of protecting physical Windows and Linux hosts. For a complete listing of available functionality see the complete Rubrik SDK for Python documentation.
Setting up the Sample Workflow

Create a file named `physicalhosts.py` in your working directory and copy in the following code:

```python
import rubrik_cdm
import urllib3

#Disable certificate warnings and connect to Rubrik Cluster
urllib3.disable_warnings()
rubrik=rubrik_cdm.Connect()

#=============================================================
# Example of adding a physical windows/linux server
#=============================================================

# Set Object Variables
server_name = "linux-1"

# Add server to Rubrik CDM
add_host = rubrik.add_physical_host(servername)

#=============================================================
# Example of creating a physical file-set
#=============================================================

# Set Object Variables
name = "Linux Home Directories"
operating_system = "Linux"
include = ['/home/','/root/']
exclude = ['*.mp3','*.mp4']
exclude_exception = ['/home/video/*.mp4']

# Create Fileset
fileset = rubrik.create_physical_fileset(name,operating_system, include, exclude, exclude_exception)

#=============================================================
# Assigning fileset to Host
#=============================================================

# Set Object Variables
server_name = "linux-1"
fileset_name = "Linux Home Directories"
operating_system = "Linux"
sla_name = "Gold"

# Assign fileset to host
assign_fileset = rubrik.assign_physical_host_fileset(server_name, fileset_name, operating_system, sla_name)
```

#### Breaking Down the Sample Workflow

After importing the needed modules, disabling certificate warnings and connecting to the Rubrik cluster, the main examples start on Line 8. 

**Lines 8 through 16** illustrate how to add a physical host to the Rubrik CDM utilizing the `add_physical_host()` function.

**Lines 18 through 30** illustrate how to create a fileset within Rubrik CDM, containing all of the inclusion and exclusion rules. The fileset is created utilizing the `create_physical_fileset()` function.

**Lines 32 through 43** complete the physical protection process by assigning both the fileset and an SLA Domain to the physical host. This is accomplished utilizing the `assign_physical_host_fileset()` function.

|Note: Functions and methods here do not reflect all of the arguments and options available. For the complete list of functionality read the complete [Rubrik SDK for Python documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python). |
| --- |

#### Running the Sample Workflow
Once `physicalhosts.py` is saved within the working directory execute the code with the following statement:

```
python physicalhosts.py
```

#### Accessing the Built-in Sample Code

To help accelerate development the Rubrik SDK for Python source contains many files containing common activities often performed against a Rubrik cluster. Sample files may be found on the [Rubrik SDK for Python GitHub page](https://github.com/rubrikinc/rubrik-sdk-for-python/tree/master/sample).

Sample code may be executed using the following syntax:

```
python samplefile.py
```

## Rubrik SDK for Python Documentation

This guide acts only as a quick start to get up and running with the Rubrik SDK for Python. For detailed information on all of the functions and features included see the complete [Rubrik SDK for Python documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python). 

## API Documentation

The Rubrik SDK for Python supports the majority of the functionality available within the Rubrik CDM. That said, the release cycles between the SDK and Rubrik CDM are not simultaneous. This means there may be times when new features or enhancements are added to the product but methods and functions to utilize them may be missing from the SDK. In these situations Python may be used to make native calls to Rubrik’s RESTful API. The following syntax outlines a common piece of Rubrik functionality, assigning a VM to an SLA Domain, however, it does so by creating raw API requests to Rubrik CDM utilizing the Python requests library:

```python
import requests
import json
import base64

auth_values = ("administrator","SuperSecret")

response = requests.get("https://192.168.150.111/api/v1/VMware/vm?name="+vmname, auth=auth_values, verify=False)
vmid = response.json()['data'][0]['id']


response = requests.get("https://192.168.150.111/api/v1/sla_domain?name="+slaname, auth=auth_values, verify=False)
slaid = response.json()['data'][0]['id']


response = requests.patch("https://192.168.150.111/api/v1/VMware/vm/"+vmid, auth=auth_values, verify=False, json={"configuredSlaDomainId": slaid })
```

Rubrik prides itself upon its API-first architecture, ensuring everything available within the HTML5 interface, and more, is consumable via a RESTful API. For more information on Rubrik’s API architecture and complete API documentation, please see the official Rubrik API Documentation.

## Troubleshooting

The Rubrik SDK for Python contains built-in functions and configurations to help assist with troubleshooting any errors that may arise.

### Enabling Logging

The `rubrik_cdm.Connect()` function contains a built-in, verbose logging mechanism which is disabled by default. To enable the logging mechanism, set the `enable_logging` argument to true when connecting to the Rubrik cluster as follows:

```python
rubrik = rubrik_cdm.Connect(enable_logging=True)
```

The `logging_level` argument can then be used to set the specific logging level you wish to use. The following levels are valid choices:

* `debug` (default value)
* `critical`
* `error`
* `warning`
* `info`

```python
rubrik = rubrik_cdm.Connect(enable_logging=True, logging_level="info")
```

When doing so, more verbose debug messages will be displayed on the console when executing various commands and functions within the Rubrik SDK for Python. For example, the `Connect()` function itself displays no information by default, however running the same function specifying enable_logging=True outputs the following:

```
[2018-08-08 09:18:59,687] [INFO] -- User Provided Node IP: 172.21.8.53
[2018-08-08 09:18:59,687] [INFO] -- Username: demo
[2018-08-08 09:18:59,687] [INFO] -- Password: *******
​
[2018-08-08 09:18:59,687] [INFO] -- cluster_node_ip: Generating a list of all Cluster Node IPs.
[2018-08-08 09:18:59,687] [INFO] -- GET https://172.21.8.53/api/internal/cluster/me/node
[2018-08-08 09:19:00,062] [INFO] -- <Response [200]>
​
```

|Note: `enable_logging` only needs to be specified on the initial connection to Rubrik when running the `Connect()` function. All subsequent calls to functions and methods within the Rubrik SDK for Python will then display verbose logging to the console thereafter. |
| --- |

## Contributing to the Rubrik SDK for Python

The Rubrik SDK for Python is hosted on a public repository on GitHub. If you would like to get involved and contribute to the SDK please follow the below guidelines.

### Common Environment Setup

1. Clone the Rubrik SDK for Python repository

```
git clone https://github.com/rubrikinc/rubrik-sdk-for-python.git
```

2. Change to the repository root directory

```
cd rubrik-sdk-for-python
```

3. Switch to the devel branch

```
git checkout devel
```

4. Create a virtual environment

For Python 3:

```
python3 -m venv venv
```

For Python 2:

```
virtualenv venv
```

5. Activate the virtual environment

```
. venv/bin/activate
```

6. Install the SDK from Source

```
python setup.py install
```


### New Function Development

The `/rubrik-sdk-for-python/rubrik_cdm` directory contains all functions for the SDK.

At a high level the directory contains the following:

* **`api.py`** - Base API Functions (get, post, etc.) that should only be touched for bug fixes.
* **`cloud.py`** - Cloud related functions
* **`cluster.py`** - Functions involving the configuration of the Rubrik cluster itself (think Day 0 configurations)
* **`data_management.py`** - Functions related to Data Protection tasks (ex. On-demand snapshots)
* **`physical.py`** - Functions involving the management of physical servers
* **`rubrik_cdm.py`** - Several internal functions as well as the Connect class which all other functions are accessed through. This should only be touched for bug fixes.

When adding a new function it ideally should be categorized to fit into one of the above files. Each function should meet the following requirements:

* Each function must be idempotent. Before making any configuration changes (post, patch, delete) you should first check to see if that change is necessary. If it's not you must return a message formatted as `No change required. {message}:`  For example, the assign_sla function first checks to see if the Rubrik object is already assigned to the provided SLA domain.
* A doc string using the docBlockr format. Visual Studio Code users can take advantage of the [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension to simplify this process.
* Each API call made in the function should have a `self.log()` call made explaining what the API call is doing. The log message should be formatted as `function_name: message`.
* A corresponding example in the `/rubrik-sdk-for-python/sample` directory named the same as the function_name.
Each function also must have associated documentation which can be auto generated through `cd docs && python create_docs.py`

Once a new function has been added you will then submit a new Pull Request which will be reviewed before merging into the devel branch.

For more information around contributing to the Rubrik SDK for Python see the [Rubrik SDK for Python Development Guide](https://github.com/rubrikinc/rubrik-sdk-for-python/blob/devel/CONTRIBUTING.md) documentation on GitHub.

## Further Reading

* [Rubrik SDK for Python GitHub Repository](https://github.com/rubrikinc/rubrik-sdk-for-python)
* [Rubrik SDK for Python Official Documentation](https://rubrik.gitbook.io/rubrik-sdk-for-python)
* [Rubrik CDM API Documentation](https://github.com/rubrikinc/api-documentation)
* [Rubrik SDK for Python Development Guide (GitHub)](https://github.com/rubrikinc/rubrik-sdk-for-python/blob/devel/CONTRIBUTING.md)
* [Hello World - Welcoming Rubrik SDK for Python](https://www.rubrik.com/blog/introducing-rubrik-python-sdk/)
