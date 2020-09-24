# add_nas_share_to_host

Add a network share to a host.

```py
def add_nas_share_to_host(self, hostname, share_type, export_point, username=None, password=None, domain=None, timeout=60):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str | The hostname or IP Address of the host serving the NAS share. |  |
| share_type  | str | The type of NAS Share you wish to backup.  | NFS, SMB |
| export_point  | str | Name of the share exported by the NAS host. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| username  | str | Username if the network share requires authentication. |  |  |
| password  | str | Password if the network share requires authentication. |  |  |
| domain  | str | Domain name of account credentials used for authentication. |  |  |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default {60}) |  |  |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The share with the given hostname and export point has already been added. |
| dict | The full API response for `POST /internal/host/share` with the given share arguments. |

## Exceptions

| Type | Message                                                                                       |
|------|-----------------------------------------------------------------------------------------------|
| InvalidParameterException | The add_nas_share_to_host() share_type argument must be one of the following: ['NFS', 'SMB']. |


## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "my_nas_host"
share_type = "NFS" # NFS or SMB
export_point = "/my_nas_share"

rubrik.add_nas_share_to_host(hostname, share_type, export_point)

```
