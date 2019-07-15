# sql_live_mount

Live Mount a mssql database from a specified recovery point i.e. data and time.
```py
def sql_live_mount(self, db_name, date, time, sql_instance=None, sql_host=None, mount_name=None, timeout=30):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| db_name  | str  | The name of the database to Live Mount. |         |
| date  | str  | The recovery_point date you wish to Live Mount formated as `Month-Day-Year` (ex: 1-15-2014).   |         |
| time  | str  | The recovery_point time you wish to Live Mount formated as `Hour:Minute AM/PM` (ex: 1:30 AM).  |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sql_instance  | str  | The SQL instance name with the database you wish to Live Mount.  |         |         |
| sql_host  | str  | The SQL Host of the database/instance to Live Mount.  |         |         |
| mount_name  | str  | The name given to the Live Mounted database i.e. AdventureWorks_Clone.  |         |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `POST /v1/mssql/db/{id}/mount`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11 AM"
db_name = "AdventureWorks2016"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
mount_name = 'AdventureWorksClone'

live_mount = rubrik.sql_live_mount(db_name, date, time, sql_instance, sql_host, mount_name)
```