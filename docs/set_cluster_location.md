# set_cluster_location

Configure the Rubrik cluster timezone.
```py
def set_cluster_location(timezone, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| location  | str  | Geolocation of the cluster.                                                   |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |
## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster is already configured with '{}' as its location. |
| dict | The full API response for `PATCH /v1/cluster/me'` |
## Example
```py
import rubrik_cdm

RubrikConn = rubrik_cdm.Connect()

RubrikConn.set_cluster_location("Example Location")
```
