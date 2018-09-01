# add_physical_host

Add a physical host from the Rubrik Cluster.
```py
def add_physical_host(hostname, timeout=60)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str  | The hostname or IP Address of the physical host you wish to add to the Rubrik Cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The timeout value for the API call that adds the physical host to the Rubrik Cluster.  |         |    60     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | If the physical host is already present on the Rubrik Cluster, a message to that effect will be retuned. |
| dict  | The response returned by the API call |
