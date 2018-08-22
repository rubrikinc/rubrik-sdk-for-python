# pause_snapshots

Pause all Snapshot activity for the provided object.

```py
def pause_snapshots(object_name, object_type, timeout=180)
```

## Arguments
object_name {str} -- The name of object (i.e vSphere VM) to pause Snaphots on.


## Keyword Arguments
object_type {str} -- The Rubrik object type you wish to pause Snaphots on. 'vmware' is currently the only supported option. (default: {vmware})

timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {180})


## Returns
str -- If the object is currently paused the following will be returned: The vSphere VM '{object_name}' is already paused.

dict -- The full response of the Instantly Recover API call.



