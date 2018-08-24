# delete_physical_host

Delete a physical host from the Rubrik Cluster.
```py
def delete_physical_host(hostname, timeout=120)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| hostname  | str  | The hostname or IP Address of the physical host you wish to remove from the Rubrik Cluster. |         |         |
| timeout  | int  | The timeout value for the API call that deletes the physical host from the Rubrik Cluster. (default: {120}) |         |    120     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | If the physical host is not present on the Rubrik Cluster, a message to that effect will be retuned. |
| dict  | The response returned by the API call. |
