# add\_physical\_host

Add a physical host to the Rubrik cluster.

```python
def add_physical_host(self, hostname, timeout=60):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| hostname | str | or \[list\]The hostname\(s\) or IP Address\(es\) of the physical host you want to add to the Rubrik cluster. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 60 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The host '`hostname`' is already connected to the Rubrik cluster. |
| dict | The full API response for `POST /v1/host`. |

## Exceptions

| Type | Message |
| :--- | :--- |
| InvalidParameterException | The provided hostname list is empty |

## Example

```python
### Single Host
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"

add_host = rubrik.add_physical_host(hostname)

### Bulk Hosts
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hosts = ['host1.rubrik.com','host2.rubrik.com','host3.rubrik.com']
bulk_add = rubrik.add_physical_host(hosts)
```

