# _time_in_range

Checks if a specific datetime exists in a start and end time. For example: checks if a recovery point exists in the available snapshots

```py
def _time_in_range(self, start, end, point_in_time):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| start  | datetime | The start time of the recoverable range the database can be mounted from. |  |
| end  | datetime | The end time of the recoverable range the database can be mounted from. |  |
| point_in_time  | datetime | The point_in_time you wish to Live Mount. |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| bool | True if point_in_time is in the range [start, end]. |



