# sql_db_export

Export an SQL database from a specified recovery point to a target SQL Instance and Host. Requires database data and log file name directory paths.
```py
    def sql_db_export(db_name, date, time, sql_instance=None, sql_host=None, target_instance_name=None, target_hostname=None, target_database_name=None, target_data_file_path=None, target_log_file_path=None, target_file_paths=None, finish_recovery=True, max_data_streams=2, allow_overwrite=False, timeout=15)
```

## Keyword Arguments
| Name                      | Type | Description                                                                 | Choices | Default |
|---------------------------|------|-----------------------------------------------------------------------------|---------|---------|
| db_name                   | str  | The name of the database to be exported.                                    |         |         |
| date                      | str  | The recovery_point date formated as `Month-Date-Year` (ex: 8-9-2018).       |         |         |
| time                      | str  | The recovery_point time formated as `Hour:Minute` (ex: 3:30 AM).            |         |         |
| sql_instance              | str  | The SQL instance name with the database to be exported.                     |         |         |
| sql_host                  | str  | The SQL Host of the database/instance to be exported.                       |         |         |
| target_instance_name      | str  | Name of the Microsoft SQL instance for the new database.                    |         |         |
| target_hostname           | str  | FName of the Microsoft SQL host for the new database.                       |         |         |
| target_database_name      | str  | Name of the new database.                                                   |         |         |
| target_data_file_path     | str  | The target path to store all data files.                                    |         |         |
| target_log_file_path      | str  | The target path to store all log files.                                     |         |         |
| target_file_paths         | list | A list of dictionary objects each with key value pairs: {'logicalName': 'Logical name of the database file', 'exportPath': 'The target path for the database file', 'newLogicalName': 'New logical name for the database file', 'newFilename': 'New filename for the database file'}. One target path for each individual database file. Overrides targetDataFilePath and targetLogFilePath.  |         |         |
| finish_recovery           | bool | A Boolean value that determines the recovery option to use during database restore. When this value is 'true', the database is restored using the RECOVERY option and is fully functional at the end of the restore operation. When this value is 'false', the database is restored using the NORECOVERY option and remains in recovering mode at the end of the restore operation. |         | True |
| max_data_streams          | int  | Maximum number of parallel data streams that can be used to copy data to the target system. |         |    2    |
| allow_overwrite           | bool | A Boolean value that determines whether an existing database can be overwritten by a database this is exported from a backup. Set to false to prevent overwrites. This is the default. Set to true to allow overwrites. |         | False |
| timeout                   | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         |    15     |

## Returns
| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full response of `POST /v1/mssql/db/{id}/export`.                                         |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
date = '10-21-2019'
time = '3:00 PM'
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'
target_instance_name = sql_instance
target_hostname = sql_host
target_database_name = 'Demo_Export'
target_data_file_path = 'C:\\Program Files\\Microsoft SQL Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export'
target_log_file_path = 'C:\\Program Files\\Microsoft SQL Server\\MSSQL13.MSSQLSERVER\\MSSQL\\DATA\\AdventureWorks2016_export'

sql_db_export = rubrik.sql_db_export(db_name,
                                     date,
                                     time,
                                     sql_instance, 
                                     sql_host,
                                     target_instance_name,
                                     target_hostname,
                                     target_database_name,
                                     target_data_file_path,
                                     target_log_file_path)
    ```
