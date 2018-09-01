# cluster_node_ip

Retrive the IP Address for each node in the Rubrik cluster.
```py
def cluster_node_ip(timeout=15)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| list  | A list that contains the IP Address for each node in the Rubrik cluster. |
