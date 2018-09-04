# get

Send a GET request to the provided Rubrik API endpoint.
```py
def get(api_version, api_endpoint, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| api_version  | str  | The version of the Rubrik CDM API to call.  |    v1, internal     |
| api_endpoint  | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |
| authentication  | bool  | Flag that specifies whether or not to utilize authentication when making the API call.  |         |    True     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response body of the API call. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

# Retrieve summary information for the "Python SDK" SLA Domain
sla_name = "Python SDK"

sla_summary_information = rubrik.get('v1', '/sla_domain?name={}'.format(sla_name))
```