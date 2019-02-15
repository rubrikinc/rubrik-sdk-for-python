# get

Send a GET request to the provided Rubrik API endpoint.
```py
def get(api_version, api_endpoint, timeout=15, authentication=True)
```

## Arguments
| Name         | Type | Description                                                   | Choices          |
|--------------|------|---------------------------------------------------------------|------------------|
| api_version  | str  | The version of the Rubrik CDM API to call.                    | v1, v2, internal |
| api_endpoint | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |                  |
## Keyword Arguments
| Name           | Type | Description                                                                                                  | Choices | Default |
|----------------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| params         | dict | An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls          |         | None    |
| timeout        | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 15      |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call.                       |         | True    |

## Returns
| Type | Return Value                       |
|------|------------------------------------|
| dict | The response body of the API call. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# Retrieve summary information for the "Python SDK" SLA Domain
sla_name = "Python SDK"

sla_summary_information = rubrik.get('v1', '/sla_domain?name={}'.format(sla_name))

# The same information but now using the optional params argument
params = {
    "name": "Python SDK"
}

sla_summary_information = rubrik.get('v1', '/sla_domain', params=params)
```