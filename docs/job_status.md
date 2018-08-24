# job_status

Certain Rubrik operations may not complete instantaneously (ex. on-demand snapshots, live mounts). In those cases we have the ability to monitor the status of the job through a job status url provided in the actions API response body. This function will perform a GET operation on the provided url and return the jobs status.
```py
def job_status(url, wait_for_completion=True, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| url  | str  | The job status URL provided by a previous API call. |         |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15}) |         |    15     |
| wait_for_completion  | bool  | Flag that determines if the method should wait for the job to complete before exiting. (default: {True}) |         |    True     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response body of the API call. |
