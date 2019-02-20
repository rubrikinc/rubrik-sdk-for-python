# patch

Send a PATCH request to the provided Rubrik API endpoint.
```py
def patch(api_version, api_endpoint, config, timeout=15, authentication=True)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| api_version  | str  | The version of the Rubrik CDM API to call.  |    v1, v2, internal     |
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
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_id = "VirtualMachine:::5008_f7c393f3-383-4b44-920-8cde7a9ae2bd:::0"

config = {}
config['configuredSlaDomainId'] = "0589c4e5-eeec-4ece-9922-2c9ceef7bec8"

change_vm_sla = rubrik.patch('v1', '/vmware/vm/{}'.format(vm_id), config)
```