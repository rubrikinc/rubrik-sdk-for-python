# _date_time_conversion

All date values returned by the Rubrik API are stored in Coordinated Universal Time (UTC) and need to be converted to the timezone configured on the Rubrik Cluster in order to match the values provided by the end user in various functions. This internal function will handle that conversion process.
```py
def _date_time_conversion(date, time)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| date  | str  | A date value formated as Month-Day-Year. Example: 1/15/2014 |         |         |
| time  | str  | A time value formated as Hour:Minute AM/PM. Example: 1:30 AM |         |         |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | A combined date/time value formated as Year-Month-DayTHour:Minute. Where Hour:Minute is on the 24-hour clock. Example: 2014-1-15T01:30 |
