# job_status

Connect to the Rubrik Cluster and get the status of a particular job.

```py
def job_status(url, wait_for_completion=True, timeout=15)
```

## Arguments
url {str} -- The job status URL provided by a previous API call.


## Keyword Arguments
timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15})

wait_for_completion {bool} -- Flag that determines if the method should wait for the job to complete before exiting. (default: {True})


## Returns
dict -- The response body of the API call.



