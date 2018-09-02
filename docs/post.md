# post

Send a POST request to the provided Rubrik API endpoint.
```py
def post(api_version, api_endpoint, config, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| api_version  | str  | The version of the Rubrik CDM API to call.  |    v1, internal     |
| api_endpoint  | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |         |
| config  | dict  | The specified data to send with the API call. |         |
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

config = {}
config['id'] = "pythonsdk"
config['password'] = "RubrikGoForward"
config['firstName'] = "Rubrik"
config['lastName'] = "Ranger"
config['emailAddress'] = "Rubrik.Ranger@pysdk.com"
config['contactNumber'] = "555-555-5555"

create_user = rubrik.post('internal', '/user', config)
```