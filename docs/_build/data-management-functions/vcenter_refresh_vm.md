# vcenter\_refresh\_vm

Refresh a single vSphere VM metadata.

```python
def vcenter_refresh_vm(self, vm_name, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| vm\_name | str | The name of the vSphere VM. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"

rubrik.vcenter_refresh_vm(vm_name)
```

