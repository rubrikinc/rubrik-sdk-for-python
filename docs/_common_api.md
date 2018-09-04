# _common_api

Internal method that consolidates the base API functions.
```py
def _common_api(call_type, api_version, api_endpoint, config=None, job_status_url=None, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| call_type  | str  | The HTTP Method for the type of RESTful API call being made.  |    'GET', 'POST', 'PATCH', 'DELETE', and 'JOB_STATUS'.     |
| api_version  | str  | The version of the Rubrik CDM API to call.  |    v1, internal     |
| api_endpoint  | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| config  | dict  | The specified data to send with `POST` and `PATCH` API calls.  |         |    None     |
| job_status_url  | str  | The job status URL provided by a previous API call.  |         |    None     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |
| authentication  | bool  | Flag that specifies whether or not to utilize authentication when making the API call.  |         |    True     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full API call response for the provided endpoint. |
