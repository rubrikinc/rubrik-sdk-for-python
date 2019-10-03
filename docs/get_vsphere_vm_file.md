# get_vsphere_vm_file

Search for a file in the snapshots of a virtual machine. Specify the file by full path prefix or filename prefix.
```py
def get_vsphere_vm_file(self, vm_name, path, timeout=15):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| vm_name  | str  | Name of the virtual machine.    |         |
| path     | str  | The path query. Use either a path prefix or a filename prefix.  |         |

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `GET /v1/vmware/vm/{id}/search?path={path}`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

path = '/etc/hosts'
vm_name = "python-sdk-demo"

get_vm_file = rubrik.get_vsphere_vm_file(vm_name, path)
```