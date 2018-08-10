# live_mount_vsphere

Create a request to Live Mount a vSphere VM from a specified Snapshot. If a specific date and time is not provided the last Snapshot taken will be selected.

```py
def live_mount_vsphere(vm_name, date='latest', time='latest', host='current', remove_network_devices=False, power_on=True)
```

## Arguments
vm_name {str} -- The name of the VM to Live Mount.


## Keyword Arguments
date {str} -- The date of the Snapshot you wish to Live Mount formated as Month-Day-Year. Example: 1/15/2014. If latest is specified the last Snapshot taken will be Live Mounted. (default: {'latest'})

time {str} -- The time of the Snapshot you wish to Live Mount formated formated as Hour:Minute AM/PM. Example: 1:30 AM. If latest is specified the last Snapshot taken will be Live Mounted. (default: {'latest'})

host {str} -- The hostname or IP address of the ESXi host to Live Mount the VM on. By default the VM will be Live Mounted to the host it is currently on. (default: {'current'})

remove_network_devices {bool} -- Determines whether to remove the network interfaces from the Live Mounted VM. Set to 'True' to remove all network interfaces. (default: {False})

power_on {bool} -- Determines whether the VM should be powered on after Live Mount. Set to 'True' to power on the VM. Set to 'False' to mount the VM but not power it on. (default: {True})


## Returns
dict -- The full response of the Live Mount API call.



