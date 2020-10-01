# \_validate\_sql\_db

Checks whether a database exist on an SQL Instance and Host.

```python
def _validate_sql_db(self, db_name, sql_instance, sql_host, timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| db\_name | str | The name of the database. |  |
| sql\_instance | str | The SQL instance. |  |
| sql\_host | str | The SQL server hostname. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | The ID of the MSSQL database. |

