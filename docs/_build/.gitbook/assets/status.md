# status

Retrieves status of in progress bootstrap requests

```py
def status(self, request_id="1", timeout=15, ipv4_addr=None):
```


## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| request_id  | str | ID of the bootstrap request |  | 1 |
| timeout  | int | The response timeout value, in seconds, of the API call.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The response returned by `GET /internal/cluster/me/bootstrap?request_id={request_id}`. |



## Example

```py
import rubrik_cdm

node_ip = '172.22.13.66'
bootstrap = rubrik_cdm.Bootstrap(node_ip)

bootstrap_status = bootstrap.status()

print(bootstrap_status)

```
