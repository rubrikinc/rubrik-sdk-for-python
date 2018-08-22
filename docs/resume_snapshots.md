# resume_snapshots

Resume all Snapshot activity for the provided object.

```py
def resume_snapshots(object_name, object_type='vmware', timeout=180)
```

## Arguments
object_name {str} -- The name of object (i.e vSphere VM) to resume Snaphots on.


## Keyword Arguments
object_type {str} -- The Rubrik object type you wish to resume Snaphots on. 'vmware' is currently the only supported option. (default: {vmware})

timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {180})


## Returns
str -- If the object is not currently paused the following will be returned: The vSphere VM '{object_name}' is currently not paused.

dict -- The full response of the Instantly Recover API call.



