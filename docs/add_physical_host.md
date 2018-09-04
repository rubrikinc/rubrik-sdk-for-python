# add_physical_host

Add a physical host to the Rubrik cluster.
```py
def add_physical_host(hostname, timeout=60)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str  | The hostname or IP Address of the physical host you want to add to the Rubrik cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    60     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change requird. The host '`hostname`' is already connected to the Rubrik cluster. |
| dict  | The full API response for `POST /v1'/host'`. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

hostname = "python-sdk-demo"

add_host = rubrik.add_physical_host(hostname)
```