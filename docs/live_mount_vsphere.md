# live_mount_vsphere

Create a request to Instantly Recover a vSphere VM from a specified Snapshot. If a specific date and time is not provided the last Snapshot taken will be selected.
```py
def live_mount_vsphere(vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| vm_name  | str  | The name of the VM to Instantly Recover. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| date  | str  | The date of the Snapshot you wish to Instantly Recover formated as Month-Day-Year. Example: 1-15-2014. If latest is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'}) |         |    'latest'     |
| time  | str  | The time of the Snapshot you wish to Instantly Recover formated formated as Hour:Minute AM/PM. Example: 1:30 AM. If latest is specified the last Snapshot taken will be Instantly Recovered. (default: {'latest'}) |         |    'latest'     |
| host  | str  | The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default the VM will be Instantly Recovered to the host it is currently on. (default: {'current'}) |         |    'current'     |
| remove_network_devices  | bool  | Determines whether to remove the network interfaces from the Instantly Recovered VM. Set to 'True' to remove all network interfaces. (default: {False}) |         |    False     |
| power_on  | bool  | Determines whether the VM should be powered on after Instantly Recover. Set to 'True' to power on the VM. Set to 'False' to mount the VM but not power it on. (default: {True}) |         |    True     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of the Instantly Recover API call. |
