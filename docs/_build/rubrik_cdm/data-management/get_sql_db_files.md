# get\_sql\_db\_files

Provides a list of database files to be restored for the specified restore or export operation. The Data, Log and Filestream files will be retrieved along with name and path information.

```python
def get_sql_db_files(self, db_name, date, time, sql_instance=None, sql_host=None, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| db\_name | str | The name of the database. |  |
| date | str | The recovery\_point date formated as 'Month-Date-Year' \(ex: 8-9-2018\). |  |
| time | str | The recovery\_point time formated as `Hour:Minute` \(ex: 3:30 AM\). |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql\_instance | str | The SQL instance name with the database. |  |  |
| sql\_host | str | The SQL Host of the database/instance. |  |  |
| timeout | int | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| list | The full response of `GET /internal/mssql/db/{id}/restore_files?time={recovery_point}`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = "10-14-2019"
time = "3:00 PM"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

get_db_files = rubrik.get_sql_db_files(db_name, date, time, sql_instance, sql_host)
```

