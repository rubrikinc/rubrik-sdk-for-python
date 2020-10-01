# sql\_live\_mount

Live Mount a database from a specified recovery point.

```python
def sql_live_mount(self, db_name, sql_instance, sql_host, mount_name, date='latest', time='latest', timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| db\_name | str | The name of the database to Live Mount. |  |
| sql\_instance | str | The SQL instance name with the database you wish to Live Mount. |  |
| sql\_host | str | The SQL Host of the database/instance to Live Mount. |  |
| mount\_name | str | The name given to the Live Mounted database i.e. AdventureWorks\_Clone. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| date | str | The recovery\_point date to recovery to formated as `Month-Day-Year` \(ex: 1-15-2014\). If `latest` is specified, the last snapshot taken will be used. |  | latest |
| time | str | The recovery\_point time to recovery to formated as `Hour:Minute AM/PM` \(ex: 1:30 AM\). If `latest` is specified, the last snapshot taken will be used. |  | latest |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `POST /v1/mssql/db/{id}/mount`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "AdventureWorks2016"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
mount_name = 'AdventureWorksClone'
date = "08-26-2018"
time = "12:11 AM"

live_mount = rubrik.sql_live_mount(db_name, sql_instance, sql_host, mount_name, date, time)
```

