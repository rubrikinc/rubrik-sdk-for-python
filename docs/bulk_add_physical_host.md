# bulk_add_physical_host

Bulk add physical hosts to the Rubrik cluster.
```py
def bulk_add_physical_host(hostnames, timeout=60)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | dict  | A list of hostnames or IP Address of the physical host you want to add to the Rubrik cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    60     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The host `hostname` is already connected to the Rubrik cluster. Removing Host and continuing" |
| dict  | The full API response for `POST 'internal/host/bulk'`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hosts = ['host1.rubrik.com','host2.rubrik.com','host3.rubrik.com']
bulk_add = rubrik.bulk_add_physical_host(hosts)
```