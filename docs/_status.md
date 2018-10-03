# _status

Internal method to retrieve the status of a `SUPPORT_BUNDLE_GENERATOR` job.
```py
def _status(bundle_job)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| bundle_job  | str  | JobID of a `SUPPORT_BUNDLE_GENERATOR` job. |         |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | The status of the `SUPPORT_BUNDLE_GENERATOR` job, or an error if the API was unable to find the JobID. |
