# on_demand_snapshot

Initiate an on-demand snapshot.
```py
def on_demand_snapshot(object_name, object_type, sla_name='current', fileset=None, host_os=None, sql_host=None, sql_instance=None, sql_db=None, hostname=None, force_full=False, share_type=None, timeout=15)
```

## Arguments
| Name        | Type | Description                                                    | Choices                    |
|-------------|------|----------------------------------------------------------------|----------------------------|
| object_name | str  | The name of the Rubrik object to take a on-demand snapshot of. |                            |
| object_type | str  | The Rubrik object type you want to backup.                     | vmware, physical_host, ahv |
## Keyword Arguments
| Name         | Type | Description                                                                                                                             | Choices        | Default |
|--------------|------|-----------------------------------------------------------------------------------------------------------------------------------------|----------------|---------|
| sla_name     | str  | The SLA Domain name you want to assign the on-demand snapshot to. By default, the currently assigned SLA Domain will be used.           |                | current |
| fileset      | str  | The name of the Fileset you wish to backup. Only required when taking a on-demand snapshot of a physical host or share.                 |                | None    |
| host_os      | str  | The operating system for the physical host. Only required when taking a on-demand snapshot of a physical host.                          | Linux, Windows | None    |
| sql_host     | str  | The name of the SQL Host hosting the specified database. Only required when taking a on-demand snapshot of a MSSQL DB.                  | None           | None    |
| sql_instance | str  | The name of the SQL Instance hosting the specified database. Only required when taking a on-demand snapshot of a MSSQL DB.              | None           | None    |
| sql_db       | str  | TThe name of the SQL DB. Only required when taking a on-demand snapshot of a MSSQL DB.                                                  | None           | None    |
| hostname     | str  | Required when the `object_type` is either `oracle_db` or `share`. When `oracle_db` is the `object_type`, this argument corresponds to the host name, or one of those host names in the cluster that the Oracle database is running. When `share` is the `object_type` this argument corresponds to the NAS server host name. | None           | None    |
| force_full   | bool | If True will force a new full image backup of an Oracle database. Used when the object_type is oracle_db                                | True, False    | False   |
| share_type   | str  | The type of NAS share i.e. NFS or SMB. Only required when taking a snapshot of a Share.                                                 | NFS or SMB    | False   |
| timeout      | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                            |                | 15      |

## Returns
| Type  | Return Value                                                                                                                                                                                             |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tuple | When object_type is vmware, the full API response for `POST /v1/vmware/vm/{ID}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url)    |
| tuple | When object_type is physical_host, the full API response for `POST /v1/fileset/{}/snapshot` and the job status URL which can be used to monitor progress of the snapshot. (api_response, job_status_url) |


## Example

### VMware

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()


vsphere_vm_name = "python-sdk-demo"
object_type = "vmware"

snapshot = rubrik.on_demand_snapshot(vsphere_vm_name, object_type)
```

### AHV

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ahv_vm_name = "python-sdk-demo"
object_type = "ahv"
snapshot = rubrik.on_demand_snapshot(ahv_vm_name, object_type)
```

### Physical Host

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

physical_host_name = "python-sdk-physical-demo"
object_type = "physical_host"
sla = "Gold"
fileset = "/etc"
host_os = "Linux"

snapshot = rubrik.on_demand_snapshot(physical_host_name, object_type, sla, fileset, host_os)
```

### MSSQL DB

#### Single/Multiple Specified DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = ["AdventureWorks2014","master"]
object_type = "mssql_db"
sql_host = "mysqlhost.rubrik.com"
sql_instance = "MSSQLSERVER"
sql_db_type = "list"
sql_ag = False
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_host=sql_host, sql_instance=sql_instance, sql_ag=sql_ag)
```

#### All User DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = None
object_type = "mssql_db"
sql_host = "mysqlhost.rubrik.com"
sql_instance = "MSSQLSERVER"
sql_db_type = "user"
sql_ag = False
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_host=sql_host, sql_instance=sql_instance, sql_db_type=sql_db_type, sql_ag=sql_ag)
```

#### All System DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = None
object_type = "mssql_db"
sql_host = "mysqlhost.rubrik.com"
sql_instance = "MSSQLSERVER"
sql_db_type = "system"
sql_ag = False
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_host=sql_host, sql_instance=sql_instance, sql_db_type=sql_db_type, sql_ag=sql_ag)
```

#### MSSQL Availability Groups - Single/Mutliple Specified DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = ["AdventureWorks2014","AdventureWorks2014v2"]
object_type = "mssql_db"
sql_instance = "MSSQLAvailabilityGroup.rubrikdemo.com"
sql_db_type = "list"
sql_ag = True
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_instance=sql_instance, sql_db_type=sql_db_type, sql_ag=sql_ag)
```

#### MSSQL Availability Groups - All User DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = None
object_type = "mssql_db"
sql_instance = "MSSQLAvailabilityGroup.rubrikdemo.com"
sql_db_type = "user"
sql_ag = True
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_instance=sql_instance, sql_db_type=sql_db_type, sql_ag=sql_ag)
```

#### MSSQL Availability Groups - All System DBs

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# MSSQL DB Snapshot
object_name = None
object_type = "mssql_db"
sql_instance = "MSSQLAvailabilityGroup.rubrikdemo.com"
sql_db_type = "system"
sql_ag = True
 
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sql_instance=sql_instance, sql_db_type=sql_db_type, sql_ag=sql_ag)
```

### Oracle DB

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = "oratestdb"
object_type = "oracle_db"
host = "ora_host_01"
sla = "OracleTest"

snapshot = rubrik.on_demand_snapshot(object_name, object_type, sla_name=sla, hostname=host, force_full=False )
```

### NAS Share

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = "python-sdk-share-demo"
object_type = "share"
sla = "Gold"
fileset = "/etc"
hostname = "python-sdk-demo"
share_type = "NFS"

snapshot = rubrik.on_demand_snapshot(object_name, object_type, sla, fileset, hostname=hostname, share_type=share_type)
```
