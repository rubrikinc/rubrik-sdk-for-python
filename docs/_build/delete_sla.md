# delete_sla

Delete an SLA from the Rubrik Cluster

```py
def delete_sla(self, name, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | [type] | The name of the SLA you wish to delete. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection to the Rubrik cluster.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full API response for `DELETE /v1/sla_domain`. |
| dict | The full API response for `DELETE /v2/sla_domain`. |



