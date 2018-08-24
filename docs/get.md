# get

Send a GET request to the provided Rubrik API endpoint.
```py
def get(api_version, api_endpoint, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| api_version  | str  | The version of the Rubrik CDM API to call. |         |         |
| api_endpoint  | str  | The endpoint (ex. cluster/me) of the Rubrik CDM API to call. |         |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15}) |         |    15     |
| authentication  | bool  | Flag that specifies whether or not to utilize authentication when making the API call. (default: {True}) |         |    True     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response body of the API call. |
