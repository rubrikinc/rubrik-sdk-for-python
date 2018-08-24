# post

Send a POST request to the provided Rubrik API endpoint.
```py
def post(api_version, api_endpoint, config, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| api_version  | str  | The version of the Rubrik CDM API to call. |         |         |
| api_endpoint  | str  | The endpoint (ex. cluster/me) of the Rubrik CDM API to call. |         |         |
| config  | dict  | The specified data to send with the API call. |         |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15}) |         |    15     |
| authentication  | bool  | Flag that specifies whether or not to utilize authentication when making the API call. (default: {True}) |         |    True     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The response body of the API call. |
