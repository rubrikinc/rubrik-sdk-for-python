# get_all_hosts

Retrieve information for each host connected to the Rubrik cluster.

```py
def get_all_hosts(self, timeout=15):
```


## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The result of the API call `GET /v1/host` |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()
host_details = rubrik.get_all_hosts()

```
