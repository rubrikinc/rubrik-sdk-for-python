# pause\_snapshots

Pause all snapshot activity for the provided object.

```python
def pause_snapshots(self, object_name, object_type, timeout=180):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| object\_name | str | The name of the Rubrik object to pause snapshots for. |  |
| object\_type | str | The Rubrik object type you wish to pause snaphots on. | vmware |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster. |  | 180 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The '`object_type`' '`object_name`' is already paused. |
| dict | The full API response for `PATCH /v1/vmware/vm/{vm_id}`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

pause_snapshot = rubrik.pause_snapshots(vm_name, object_type)
```

