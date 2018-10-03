# get_events

Return a list of Events matching the specified criteria.
```py
def get_events(limit=10, status=None, event_type=None, object_type=None, object_name=None, before_date=None, after_date=None)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| limit  | int  | The limit of Events to return.  |    1-15     |    10      |
| status  | str  | Filter the events by Status.  |    Failure, Warning, Running, Success, Canceled, Canceling     |    None      |
| event_type  | str  | Filter the events by Event Type.  |    Archive Audit, AuthDomain, Backup, CloudNativeSource, Configuration, Diagnostic, Instantiate, Maintenance, NutanixCluster, Recovery, Replication, StorageArray, System, Vcd, VCenter     |    None      |
| object_type  | str  | Filter the events by Object Type.  |    VmwareVm, Mssql, LinuxFileset, WindowsFileset, WindowsHost, LinuxHost, StorageArrayVolumeGroup, VolumeGroup, NutanixVm, AwsAccount, Ec2Instance     |    None      |
| object_name  | str  | Filter the events by Object Name.  |    Can be the name of a VM, Host, Fileset, Mssql Database, etc     |    None      |
| before_date  | datetime  | Only show events before specified date.  |    E.g. 2018-10-01     |    None      |
| after_date  | datetime  | Only show events after specified date.  |    E.g. 2018-10-01     |    None      |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The `data` object within the API response for `GET /internal/event/` after applying the specified filters. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

events = rubrik.get_events()
```