# get_events

Return a list of Events matching the specified criteria.
```py
def get_events(limit=10, status="", event_type="")
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| limit (optional - defaults to 10)  | int  | The limit of Events to return. Accepted limit is between 1-15. |         |
| status (optional)  | str  | Filter the events by Status (Choices: {Failure}, {Warning}, {Running}, {Success}, {Canceled}, {Canceling}) |         |
| event_type (optional)  | str  | Filter the events by Event Type (Choices: {Archive}, {Audit}, {AuthDomain}, {Backup}, {CloudNativeSource}, {Configuration}, {Diagnostic}, {Instantiate}, {Maintenance}, {NutanixCluster}, {Recovery}, {Replication}, {StorageArray}, {System}, {Vcd}, {VCenter}) |         |
| object_type (optional)  | str  | Filter the events by Object Type (Choices: {VmwareVm}, {Mssql}, {LinuxFileset}, {WindowsFileset}, {WindowsHost}, {LinuxHost}, {StorageArrayVolumeGroup}, {VolumeGroup}, {NutanixVm}, {AwsAccount}, {Ec2Instance}) |         |

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