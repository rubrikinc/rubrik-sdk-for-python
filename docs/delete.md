# delete

Send a DELETE request to the provided Rubrik API endpoint.
```py
def delete(api_version, api_endpoint, timeout=15, authentication=True)
```

## Arguments
| Name         | Type | Description                                                   | Choices          |
|--------------|------|---------------------------------------------------------------|------------------|
| api_version  | str  | The version of the Rubrik CDM API to call.                    | v1, v2, internal |
| api_endpoint | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |                  |
## Keyword Arguments
| Name           | Type | Description                                                                                                                  | Choices | Default |
|----------------|------|------------------------------------------------------------------------------------------------------------------------------|---------|---------|
| params         | dict | An optional dict containing variables in a key:value format to send with `DELETE` API calls. Mutually exclusive with config. |         | None    |
| config         | dict | The specified data to send with `DELETE` API calls. Mutually exclusive with params.                                          |         | None    |
| timeout        | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                 |         | 15      |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call.                                       |         | True    |

## Returns
| Type | Return Value                       |
|------|------------------------------------|
| dict | The response body of the API call. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# Delete an SLA Domain from the Rubrik cluster
sla_id = "0589c4e5-eeec-4ece-9922-2c9ceef7bec8"

delete_sla = rubrik.delete('v1', '/sla_domain/{}'.format(sla_id))
```