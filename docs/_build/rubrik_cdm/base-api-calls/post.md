# post

Send a POST request to the provided Rubrik API endpoint.

```python
def post(self, api_version, api_endpoint, config, timeout=15, authentication=True):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| api\_version | str | The version of the Rubrik CDM API to call. | v1, v2, internal |
| api\_endpoint | str | The endpoint of the Rubrik CDM API to call \(ex. /cluster/me\). |  |
| config | dict | The specified data to send with the API call. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call. |  | True |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The response body of the API call. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

config = {}
config['id'] = "pythonsdk"
config['password'] = "RubrikGoForward"
config['firstName'] = "Rubrik"
config['lastName'] = "Ranger"
config['emailAddress'] = "Rubrik.Ranger@pysdk.com"
config['contactNumber'] = "555-555-5555"

create_user = rubrik.post('internal', '/user', config)
```

