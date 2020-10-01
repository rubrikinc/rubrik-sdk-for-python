# get\_sql\_live\_mount

Retrieve the Live Mounts for a MSSQL source database.

```python
def get_sql_live_mount(self, db_name, sql_instance=None, sql_host=None, timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| db\_name | str | The name of the source database with Live Mounts. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql\_instance | str | The SQL instance name of the source database. |  |  |
| sql\_host | str | The SQL host name of the source database/instance. |  |  |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `GET /v1/mssql/db/mount?source_database_id={id}`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

get_live_mount = rubrik.get_sql_live_mount(db_name, sql_instance, sql_host)
```

