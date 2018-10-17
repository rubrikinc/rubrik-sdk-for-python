# cluster_version

Retrieves the software version of the Rubrik cluster.
```py
def cluster_version(timeout=15)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | The version of CDM installed on the Rubrik cluster. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_version = rubrik.cluster_version()
```