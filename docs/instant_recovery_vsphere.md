# instant_recovery_vsphere

Instantly recovery a virtual machine from a snapshot. If a specific date and time is not provided the last Snapshot taken will be selected.
```py
def instant_recovery_vsphere(vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True, disable_network=False, keep_mac_addresses=False, preserve_moid=False)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| vm_name  | str  | The name of the VM to Instantly Recover. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| date  | str  | The date of the Snapshot you wish to Instantly Recover formated as Month-Day-Year. Example: 1-15-2014. If 'latest' is specified the last Snapshot taken will be Instantly Recovered.  |         |    latest     |
| time  | str  | The time of the Snapshot you wish to Instantly Recover formated formated as Hour:Minute AM/PM. Example: 1:30 AM. If 'latest' is specified the last Snapshot taken will be Instantly Recovered.  |         |    latest     |
| host  | str  | The hostname or IP address of the ESXi host to Instantly Recover the VM on. By default the VM will be Instantly Recovered to the host it is currently on.  |         |    current     |
| remove_network_devices  | bool  | Determines whether to remove the network interfaces from the Instantly Recovered VM. Set to 'True' to remove all network interfaces.  |         |    False     |
| power_on  | bool  | Determines whether the VM should be powered on after Instant Recovery. Set to 'True' to power on the VM. Set to 'False' to mount the VM but not power it on.  |         |    True     |
| disable_network  | bool  | Sets the state of the network interfaces when the VM is mounted. Use 'False' to enable the network interfaces. Use 'True' to disable the network interfaces. Disabling the interfaces can prevent IP conflicts.  |         |    False     |
| keep_mac_addresses  | bool  | Determines whether the MAC addresses of the network interfaces on the source VM are assigned to the new VM. Set to 'True' to assign the original MAC addresses to the new VM. Set to 'False' to assign new MAC addresses. When 'remove_network_devices' is set to 'True', this property is ignored.  |         |    False     |
| preserve_moid  | bool  | Determines whether to preserve the MOID of the source VM in a restore operation. Use 'True' to keep the MOID of the source. Use 'False' to assign a new moid.  |         |    False     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of the Instantly Recover API call. |
