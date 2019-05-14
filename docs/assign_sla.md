# assign_sla

Assign a Rubrik object to an SLA Domain.
```py
def assign_sla(object_name, sla_name, object_type, timeout=30)
```

## Arguments
| Name                            | Type | Description                                                                                                                                                                                                                                                | Choices            |
|---------------------------------|------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|
| object_name                     | str  | The name of the Rubrik object you wish to assign to an SLA Domain.                                                                                                                                                                                         |                    |
| sla_name                        | str  | The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use `do not protect` as the `sla_name`. To assign the selected object to the SLA of the next higher level object use `clear` as the `sla_name`. |                    |
| object_type                     | str  | The Rubrik object type you want to assign to the SLA Domain.                                                                                                                                                                                               | vmware, mssql_host |
| log_backup_frequency_in_seconds | int  | (Optional) The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`.                                                                                                                             |                    |
| log_retention_hours             | int  | (Optional) The MSSQL Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`.                                                                                                                          |                    |
| copy_only                       | bool | (Optional) Take Copy Only Backups with MSSQL. Required when the `object_type` is `mssql_host`.                                                                                                                                                             |                    |
## Keyword Arguments
| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| timeout | str  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 30      |

## Returns
| Type | Return Value                                                                                           |
|------|--------------------------------------------------------------------------------------------------------|
| str  | No change required. The vSphere VM '`object_name`' is already assigned to the '`sla_name`' SLA Domain. |
| dict | The full API reponse for `POST /internal/sla_domain/{sla_id}/assign`.                                  |

## Example
### VMware
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
sla_name = "Gold"
object_type = "vmware"

assign_sla = rubrik.assign_sla(vm_name, sla_name, object_type)
```
### MSSQL
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk.demo.com'
object_type = 'mssql_host'

sla_name = 'Gold'
log_backup_frequency_in_seconds = 600
log_retention_hours = 12
copy_only = False

assignsla = rubrik.assign_sla(object_name, sla_name, object_type, logBackupFrequencyInSeconds, logRetentionHours, copyOnly)
```
