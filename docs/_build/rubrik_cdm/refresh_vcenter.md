# refresh_vcenter

Refresh the metadata for the specified vCenter Server.

```py
def refresh_vcenter(self, vcenter_ip, wait_for_completion=True, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| vcenter_ip  | str | The IP address or FQDN of the vCenter you wish to refesh. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| wait_for_completion  | bool | Flag to determine if the function should wait for the refresh to complete before completing.  |  | True |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | When wait_for_completion is False, the full API response for `POST /v1/vmware/vcenter/{id}/refresh` |
| dict | When wait_for_completion is True, the full API response of the job status |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vcenter_hostname = "python.demo.lab"

refresh = rubrik.refresh_vcenter(vcenter_hostname)

print(refresh)

```
