# get_sql_live_mount

Retrieve the Live Mounts for a MSSQL source database.
```py
def sql_live_mount(self, db_name, sql_instance=None, sql_host=None, timeout=30):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| db_name  | str  | The name of the source database with Live Mounts. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sql_instance  | str  | The SQL instance name of the source database.  |         |    None     |
| sql_host  | str  | The SQL host name of the source database/instance.  |         |     None    |
| mount_name  | str  | The name given to the Live Mounted database i.e. AdventureWorks_Clone.  |         |    None     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `GET /v1/mssql/db/mount?source_database_id={id}`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

get_live_mount = rubrik.get_sql_live_mount(db_name, sql_instance, sql_host)
```