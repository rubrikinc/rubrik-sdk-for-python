# resume\_snapshots

Resume all snapshot activity for the provided object.

```python
def resume_snapshots(self, object_name, object_type, timeout=180):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| object\_name | str | The name of the Rubrik object to resume snapshots for. |  |
| object\_type | str | The Rubrik object type you wish to resume snaphots on. | vmware |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster. |  | 180 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The 'object\_type' object 'object\_name' is currently not paused. |
| dict | The full response for `PATCH /v1/vmware/vm/{vm_id}`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

resume_snapshot = rubrik.resume_snapshots(vm_name, object_type)
```

