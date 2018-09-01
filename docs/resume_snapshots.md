# resume_snapshots

Resume all snapshot activity for the provided object.
```py
def resume_snapshots(object_name, object_type, timeout=180)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the Rubrik object (i.e vSphere VM, Fileset, etc.) to resume snapshots for. |         |
| object_type  | str  | The Rubrik object type you wish to resume Snaphots on.  |    vmware     |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster.  |         |    180     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The 'object_type' object 'object_name' is currently not paused. |
| dict  | The full response for `PATCH /v1/vmware/vm/{vm_id}`. |
