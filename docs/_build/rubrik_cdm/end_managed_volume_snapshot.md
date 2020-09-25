# end_managed_volume_snapshot

Close a managed volume for writes. A snapshot will be created containing all writes since the last begin snapshot call.

```py
def end_managed_volume_snapshot(self, name, sla_name='current', timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str | The name of the Managed Volume to end snapshots on. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sla_name  | str | The SLA Domain name you want to assign the snapshot to. By default, the currently assigned SLA Domain will be used.  |  | current |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The Managed Volume `name` is already assigned in a read only state. |
| dict | The full API response for `POST /managed_volume/{id}/end_snapshot`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

managed_volume_name = 'MV1'

end_snapshot = rubrik.end_managed_volume_snapshot(managed_volume_name)

print(end_snapshot)

```
