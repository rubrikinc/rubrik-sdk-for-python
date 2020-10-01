# put

Send a PUT request to the provided Rubrik API endpoint.

```py
def put(self, api_version, api_endpoint, config, timeout=15, authentication=True):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| api_version  | str | The version of the Rubrik CDM API to call.  | v1, v2, internal |
| api_endpoint  | str | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |  |
| config  | dict | The specified graphql to send with the API call. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |
| authentication  | bool | Flag that specifies whether or not to utilize authentication when making the API call.  |  | True |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The response body of the API call. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()


config = {}
config['loginBanner'] = "Login Banner for the Python SDK Cluster"


set_login_banner = rubrik.put('internal', '/cluster/me/login_banner', config)
```
