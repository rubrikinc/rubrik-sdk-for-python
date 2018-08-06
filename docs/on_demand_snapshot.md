# on_demand_snapshot()

Initiate an on-demand snapshot.

```py
def on_demand_snapshot(object_name, object_type=None, sla_name='current')
```

## Arguments
object_name {str} -- The name of object (i.e vSphere VM, Fileset, etc.) to take a Snapshot of.


## Keyword Arguments
object_type {str} -- The Rubrik object type you wish to backup. vmware is currently the only supported option. (default: {None})

sla_name {str} -- The SLA Domain name you to assign the snapshot to. By default the currently assigne SLA Domain will be used. (default: {'current'})


## Returns
tuple -- The full API response and the job status URL which can be used to monitor progress of the Snapshot. (api_response, job_status_url)



