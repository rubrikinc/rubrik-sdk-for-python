# configure_cluster_location

Configure the Rubrik cluster timezone.
```py
def configure_cluster_location(location, timeout=15)
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
| str  | No change required. The Rubrik cluster is already configured with 'location' as its location. |
| dict | The full API response for `PATCH /v1/cluster/me'` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

rubrik.configure_cluster_location("St. Louis, Missouri")
```
