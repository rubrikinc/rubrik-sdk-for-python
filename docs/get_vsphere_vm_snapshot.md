# get_vsphere_vm_snapshot

Retrieve summary information for the snapshots of a virtual machine.
```py
def get_vsphere_vm_snapshot(self, id, timeout=15):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| id  | str  | ID of the virtual machine.    |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `GET /v1/vmware/vm/{id}/snapshot`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

id = "VirtualMachine:::ID"

get_vm_snapshot = rubrik.get_vsphere_vm_snapshot(id=id)
```