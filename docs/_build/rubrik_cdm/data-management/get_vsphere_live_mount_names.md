# get\_vsphere\_live\_mount\_names

Get existing Live Mount VM name\(s\) for a vSphere VM.

```python
def get_vsphere_live_mount_names(self, vm_name, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| vm\_name | str | The name of the mounted vSphere VM. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| list | A list of the Live Mounted VM names. |

## Example

```python
import rubrik_cdm

vm_name = "python-sdk-demo"

rubrik = rubrik_cdm.Connect()

live_mount = rubrik.get_vsphere_live_mount_names(vm_name)
```

