# vsphere_live_mount

Live Mount a vSphere VM from a specified snapshot. If a specific date and time is not provided, the last snapshot taken will be used.
```py
def vsphere_live_mount(vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| vm_name  | str  | The name of the vSphere VM to Live Mount. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| date  | str  | The date of the snapshot you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014). If `latest` is specified, the last snapshot taken will be used.  |         |    latest     |
| time  | str  | The time of the snapshot you wish to Live Mount formated formated as `Hour:Minute AM/PM` (ex: 1:30 AM). If `latest` is specified, the last snapshot taken will be used.  |         |    latest     |
| host  | str  | The hostname or IP address of the ESXi host to Live Mount the VM on. By default, the current host will be used.  |         |    current     |
| remove_network_devices  | bool  | Flag that determines whether to remove the network interfaces from the Live Mounted VM. Set to `True` to remove all network interfaces.  |         |    False     |
| power_on  | bool  | Flag that determines whether the VM should be powered on after the Live Mount. Set to `True` to power on the VM. Set to `False` to mount the VM but not power it on.  |         |    True     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `POST /v1/vmware/vm/snapshot/{snapshot_id}/mount`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11 AM"

live_mount = rubrik.vsphere_live_mount(vm_name, date, time)
```