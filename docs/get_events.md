# get_events

Return a list of Events matching the specified criteria.
```py
def get_events(limit=10, status=None, event_type=None, object_type=None, object_name=None, before_date=None, after_date=None)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| limit  | int  | The limit of Events to return. Accepted limit is between 1-15. (Default 10) |         |         |
| status  | str  | Filter the events by Status (Choices: {Failure}, {Warning}, {Running}, {Success}, {Canceled}, {Canceling}) |         |         |
| event_type  | str  | Filter the events by Event Type (Choices: {Archive}, {Audit}, {AuthDomain}, {Backup}, {CloudNativeSource}, {Configuration}, {Diagnostic}, {Instantiate}, {Maintenance}, {NutanixCluster}, {Recovery}, {Replication}, {StorageArray}, {System}, {Vcd}, {VCenter}) |         |         |
| object_type  | str  | Filter the events by Object Type (Choices: {VmwareVm}, {Mssql}, {LinuxFileset}, {WindowsFileset}, {WindowsHost}, {LinuxHost}, {StorageArrayVolumeGroup}, {VolumeGroup}, {NutanixVm}, {AwsAccount}, {Ec2Instance}) |         |         |
| object_name  | str  | Filter the events by Object Name (Can be the name of a VM, Host, Fileset, Mssql Database, etc) |         |         |
| before_date  | datetime  | Only show events before specified date. (Ex. 2018-10-01) |         |         |
| after_date  | datetime  | Only show events after specified date. (Ex. 2018-10-01) |         |         |

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