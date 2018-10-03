# _db_u_bun_state

Internal method to update the local internal database with the status of the Bundle.
```py
def _db_u_bun_state(job_id, bun_status)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| job_id  | str  | JobID of the `SUPPORT_BUNDLE_GENERATOR` job. |         |
| bun_status  | str  | Status of the Bundle (`GENERATING` / `DOWNLOADED`). |         |
