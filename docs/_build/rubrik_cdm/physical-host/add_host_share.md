# add\_host\_share

Add a network share object to a host.

```python
def add_host_share(self, hostname, share_type, export_point, username=None, password=None, domain=None, timeout=60):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| hostname | str | The hostname or IP Address of the physical host you want to add to the Rubrik cluster. |  |
| share\_type | str | The share object type to be added to the host. | NFS, SMB |
| export\_point | str | The NFS export path of the share. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| username | str | The username for the host. |  | None |
| password | str | The password for the host. |  | None |
| domain | str | The domain for the host |  | None |
| timeout | int | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |  | 60 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full API response for `POST /internal/host/share`. |

## Example

```python
import rubrik_cdm

hostname = 'nas-server.rubrikdemo.com'
share_type = 'NFS'
export_point = '/nas_share'

rubrik = rubrik_cdm.Connect()

add_host_share = rubrik.add_host_share(hostname, share_type, export_point)
```

