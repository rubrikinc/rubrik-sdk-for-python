# \_validate\_sql\_recovery\_point

Check whether the data and time provided is a valid recovery point for an MSSQL database

```python
def _validate_sql_recovery_point(self, mssql_id, date, time, timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| mssql\_id | str | The ID of the database. |  |
| date | str | The recovery\_point date formated as `Month-Day-Year` \(ex: 1-15-2014\). |  |
| time | str | The recovery\_point time  formated as `Hour:Minute AM/PM` \(ex: 1:30 AM\). |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 30 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | A dictionary with values {'is\_recovery\_point': bool, 'recovery\_timestamp': datetime}. |

