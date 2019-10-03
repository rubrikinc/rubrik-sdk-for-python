# get_vsphere_vm_file

Search for a file in the snapshots of a virtual machine. Specify the file by full path prefix or filename prefix.
```py
def get_vsphere_vm_file(self, id, path=None, timeout=15):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| id  | str  | ID of the virtual machine.    |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| path     | str  | The path query. Use either a path prefix or a filename prefix.  |         |    None     |
| timeout  | int  | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `GET /v1/vmware/vm/{id}/search?path={path}`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

id = "VirtualMachine:::ID"
path = '/etc/hosts'

get_vm_file = rubrik.get_vsphere_vm_file(id=id, path=path)
```