# pause_snapshots

Pause all snapshot activity for the provided object.
```py
def pause_snapshots(object_name, object_type, timeout=180)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the Rubrik object (i.e vSphere VM, Fileset, etc.) to pause snapshots for. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| object_type  | str  | The Rubrik object type you wish to pause snaphots on. (choices: {vmware}) |    vmware     |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster.  |         |    180     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The vSphere VM '`object_name`' is already paused. |
| dict  | The full API response for `PATCH /v1/vmware/vm/{vm_id}'. |
