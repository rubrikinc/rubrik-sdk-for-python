# delete_physical_host

Delete a physical host from the Rubrik cluster.
```py
def delete_physical_host(hostname, timeout=120)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str  | The hostname or IP Address of the physical host you wish to remove from the Rubrik cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    120     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The host '`hostname`' is not connected to the Rubrik cluster. |
| dict  | The full API response for `DELETE /v1'/host/{host_id}`. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

hostname = "python-sdk-demo"

delete_host = rubrik.delete_physical_host(hostname)
```