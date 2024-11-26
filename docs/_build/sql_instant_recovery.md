# sql_instant_recovery

Perform an instant recovery for MSSQL database from a specified recovery point.

```py
def sql_instant_recovery(self, db_name, date, time, sql_instance=None, sql_host=None, finish_recovery=True, max_data_streams=0, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| db_name  | str | The name of the database to instantly recover. |  |
| date  | str | The recovery_point date to recover to formated as `Month-Day-Year` (ex: 1-15-2014). |  |
| time  | str | The recovery_point time to recover to formated as `Hour:Minute:Second AM/PM` (ex: 1:30 AM). |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sql_instance  | str | The SQL instance name with the database to instantly recover. |  |  |
| sql_host  | str | The SQL Host of the database/instance to instantly recover. |  |  |
| finish_recovery  | bool | A Boolean value that determines the recovery option to use during database restore. When this value is 'true', the database is restored using the RECOVERY option and is fully functional at the end of the restore operation. When this value is 'false', the database is restored using the NORECOVERY option and remains in recovering mode at the end of the restore operation. |  |  |
| max_data_streams  | int | Maximum number of parallel data streams that can be used to copy data to the target system. |  |  |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full response of `POST /v1/mssql/db/{id}/restore`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11:00 AM"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
mount_name = 'AdventureWorksClone'
finish_recovery = True
max_data_streams = 0

live_mount = rubrik.sql_instant_recovery(db_name, date, time, sql_instance, sql_host, finish_recovery, max_data_streams)
```
