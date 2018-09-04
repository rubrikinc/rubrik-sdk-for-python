# job_status

Certain Rubrik operations (on-demand snapshots, live mounts, etc.) may not complete instantaneously. In those cases we have the ability to monitor the status of the job through a job status url provided in the actions API response body. This function will perform a GET operation on the provided url and return the jobs status.
```py
def job_status(url, wait_for_completion=True, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| url  | str  | The job status URL provided by a previous API call. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |
| wait_for_completion  | bool  | Flag that determines if the method should wait for the job to complete before exiting.  |         |    True     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response body of the API call. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

# Monitor the progress of a On-Demand Snapshot
job_status_url = "https://172.21.8.52/api/v1/vmware/vm/request/CREATE_VMWARE_SNAPSHOT_fase1f32-3872-2982-a68c-6fe145982f48-vm-5008_f7c393f3-383-4b44-920-8cde7a9ae2bd:::0"

snapshot_status = rubrik.job_status(job_status_url)
```