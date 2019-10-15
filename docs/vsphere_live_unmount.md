# vsphere_live_unmount

Delete a vSphere Live Mount from the Rubrik cluster.
```py
def vsphere_live_unmount(mounted_vm_name, force=False, timeout=30)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| mounted_vm_name  | str  | The name of the Live Mounted vSphere VM to be unmounted. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| force  | bool  | Force unmount to remove metadata when the datastore of the Live Mount virtual machine was moved off of the Rubrik cluster.  |         |    False     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `DELETE /vmware/vm/snapshot/mount/{id}?force={bool}`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

mounted_vm_name = "python-sdk-demo"

live_unmount = rubrik.vsphere_live_unmount(mounted_vm_name)
```