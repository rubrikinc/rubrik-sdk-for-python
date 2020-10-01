# cluster\_node\_id

Returns a list of node ids from all the nodes in the cluster.

```python
def cluster_node_id(self, timeout=15):
```

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| list | A list that contains the ID for each node in the Rubrik cluster. |

## Example

```python
import rubrik_cdm, urllib3

urllib3.disable_warnings()

rubrik = rubrik_cdm.Connect(rubrik_cdm_ip, rubrik_cdm_user_name, rubrik_cdm_password)

ids = rubrik.cluster_node_id()
print(ids)
```

