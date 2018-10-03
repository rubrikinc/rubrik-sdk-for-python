# _db_d_event_id

Internal method to delete an EventID from the local internal database due to `SUPPORT_BUNDLE_GENERATOR` job failure or age.
```py
def _db_d_event_id(event_id)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| event_id  | str  | EventID to remove from the database. |         |
