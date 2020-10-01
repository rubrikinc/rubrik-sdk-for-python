# \_date\_time\_conversion

All date values returned by the Rubrik API are stored in Coordinated Universal Time \(UTC\) and need to be converted to the timezone configured on the Rubrik cluster in order to match the values provided by the end user in various functions. This internal function will handle that conversion process.

```python
def _date_time_conversion(self, date, time, timeout=30):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| date | str | A date value formated as `Month-Day-Year` \(ex: 1/15/2014\). |  |
| time | str | A time value formated as `Hour:Minute AM/PM` \(ex: 1:30 AM\). |  |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | A combined date/time value formated as `Year-Month-DayTHour:Minute` where Hour:Minute is on the 24-hour clock \(ex : 2014-1-15T01:30\). |

