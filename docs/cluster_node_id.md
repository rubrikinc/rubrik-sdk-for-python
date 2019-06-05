# cluster_node_id

Returns a list of node ids from all the nodes in the cluster.
```py
def cluster_node_id(timeout=15)
```

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns

| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full API response from `POST /internal/node`. |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_node_id = rubrik.cluster_node_id()
```
