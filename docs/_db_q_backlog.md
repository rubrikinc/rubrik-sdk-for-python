# _db_q_backlog

Internal method to query the local internal database for all existing EventIDs that have pending `SUPPORT_BUNDLE_GENERATOR` jobs.
```py
def _db_q_backlog()
```


## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| tuple  | The row(s) from the database containing EventIDs with `SUPPORT_BUNDLE_GENERATOR` jobs in a `GENERATING` status. |
