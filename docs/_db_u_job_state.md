# _db_u_job_state

Internal method to update the local internal database with the status of the `SUPPORT_BUNDLE_GENERATOR` job.
```py
def _db_u_job_state(job_id, job_state)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| job_id  | str  | JobID of the `SUPPORT_BUNDLE_GENERATOR` job. |         |
| job_state  | str  | Status of the `SUPPORT_BUNDLE_GENERATOR` job as retrieved from the `/internal/support/support_bundle` endpoint. |         |
