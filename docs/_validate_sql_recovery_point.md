# _validate_sql_recovery_point

Check whether the data and time provided is a valid recovery point for an MSSQL database
```py
def _validate_sql_recovery_point(db_name, date, time, timeout=30)
```

## Arguments
| Name        | Type | Description                                                           | Choices |
|-------------|------|-----------------------------------------------------------------------|---------|
| db_name  | str  | The name of the database.                                                |         |
| date     | str  | The recovery_point date formated as `Month-Day-Year` (ex: 1-15-2014).    |         |
| time     | str  | The recovery_point time  formated as `Hour:Minute AM/PM` (ex: 1:30 AM).  |         |

## Keyword Arguments
| Name           | Type | Description                                                         | Choices | Default |
|----------------|------|---------------------------------------------------------------------|---------|---------|
| timeout        | int  | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |         | 30      |

## Returns
| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | A dictionary with values {'is_recovery_point': bool, 'recovery_timestamp': datetime}.         |
