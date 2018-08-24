# bootstrap_status

Retrieves status of in progress bootstrap requests
```py
def bootstrap_status(request_id="1", timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| request_id  | str  | Id of the bootstrap request (default: {"1"}) |         |    "1"     |
| timeout  | int  | The response timeout value, in seconds, of the API call. (default: {15}) |         |    15     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response returned by the API call. |
