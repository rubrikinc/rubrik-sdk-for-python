# get_all_vcenters

Retrieve information for each vCenter connected to the Rubrik cluster.

```py
def get_all_vcenters(self, timeout=15):
```


## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full API response for `GET /v1/vmware/vcenter`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()
vcenter_details = rubrik.get_all_vcenters()

```
