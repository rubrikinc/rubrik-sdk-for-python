# get\_vsphere\_vm\_details

Retrieve details for a virtual machine.

```python
def get_vsphere_vm_details(self, vm_name, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| vm\_name | str | Name of the virtual machine. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `GET /v1/vmware/vm/{vm_id}` |

## Example

```python
import rubrik_cdm

vm_name = "python-sdk-demo"

rubrik = rubrik_cdm.Connect()

get_vm_details = rubrik.get_vsphere_vm_details(vm_name)
```

