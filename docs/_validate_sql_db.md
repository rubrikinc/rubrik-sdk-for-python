# _validate_sql_db

Checks whether a database exist on an SQL Instance and Host.
```py
def _validate_sql_db(db_name, sql_instance, sql_host, timeout=30)
```

## Arguments
| Name        | Type | Description                                                           | Choices |
|-------------|------|-----------------------------------------------------------------------|---------|
| db_name  | str  | The name of the database.                                                |         |
| sql_instance   | str  | The SQL instance.                                                   |         |     
| sql_host       | str  | The SQL server hostname.                                            |         | 
## Keyword Arguments
| Name           | Type | Description                                                         | Choices | Default |
|----------------|------|---------------------------------------------------------------------|---------|---------|
| timeout        | int  | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |    | 30      |

## Returns
| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str  | The ID of the MSSQL database.                                                                 |
