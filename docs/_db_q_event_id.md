# _db_q_event_id

Internal method to query the local internal database for existing EventIDs so that duplicate generation jobs are not executed.
```py
def _db_q_event_id(event_id)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| event_id  | str  | The `eventSeriesId` returned by the `/internal/event` endpoint. |         |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| tuple  | The row(s) from the database containing the EventID in question. |
