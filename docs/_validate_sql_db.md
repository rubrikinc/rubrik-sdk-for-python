# _validate_sql_db

Checks whether a database exist on an SQL Instance and Host.
```py
def _validate_sql_db(db_name, sql_instance=None, sql_host=None, timeout=30)
```

## Arguments
| Name        | Type | Description                                                           | Choices |
|-------------|------|-----------------------------------------------------------------------|---------|
| db_name  | str  | The name of the database.                                                |         |

## Keyword Arguments
| Name           | Type | Description                                                         | Choices | Default |
| sql_instance   | str  | The SQL instance.                                                   |         | None    |
| sql_host       | str  | The SQL server hostname.                                            |         | None    |
| timeout        | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 30      |

## Returns
| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str  | The ID of the MSSQL database.                                                                 |
