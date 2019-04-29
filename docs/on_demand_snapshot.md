# on_demand_snapshot

Initiate an on-demand snapshot.
```py
def on_demand_snapshot(object_name, object_type, sla_name='current', fileset=None, host_os=None, sql_host=None, sql_instance=None, sql_db=None, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the Rubrik object to take a on-demand snapshot of. |         |
| object_type  | str  | The Rubrik object type you want to backup.  |    vmware, physical_host, ahv     |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sla_name  | str  | The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used.  |         |    current     |
| fileset  | str  | The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host.  |         |    None     |
| host_os  | str  | The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host.  |    Linux, Windows     |    None      |
| sql_host  | str  | The name of the SQL Host hosting the specified database. Only required when taking a on-demand snapshot of a MSSQL DB.  |    None     |    None      |
| sql_instance  | str  | The name of the SQL Instance hosting the specified database. Only required when taking a on-demand snapshot of a MSSQL DB.  |    None     |    None      |
| sql_db  | str  | TThe name of the SQL DB. Only required when taking a on-demand snapshot of a MSSQL DB.  |    None     |    None      |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| tuple  | When object_type is vmware, the full API response for `POST /v1/vmware/vm/{ID}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url) |
| tuple  | When object_type is physical_host, the full API response for `POST /v1/fileset/{}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url) |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# VMware Snapshot
vsphere_vm_name = "python-sdk-demo"
object_type = "vmware"
snapshot = rubrik.on_demand_snapshot(vsphere_vm_name, object_type)

# AHV Snapshot
ahv_vm_name = "python-sdk-demo"
object_type = "ahv"
snapshot = rubrik.on_demand_snapshot(ahv_vm_name, object_type)

# Physical Host Snapshot
physical_host_name = "python-sdk-physical-demo"
object_type = "physical_host"
sla = "Gold"
fileset = "/etc"
host_os = "Linux"

snapshot = rubrik.on_demand_snapshot(physical_host_name, object_type, sla, fileset, host_os)

# MSSQL DB Snapshot
object_name = "AdventureWorks2014"
object_type = "mssql_db"

snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_host="hostname.rubrik.com", sql_instance="MSSQLSERVER", sql_db="AdventureWorks2014")
```