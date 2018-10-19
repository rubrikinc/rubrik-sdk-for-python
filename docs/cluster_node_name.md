# cluster_node_name

Retrive the name of each node in the Rubrik cluster.
```py
def cluster_node_name(timeout=15)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| list  | A list that contains the name of each node in the Rubrik cluster. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

node_names = rubrik.cluster_node_name()
```