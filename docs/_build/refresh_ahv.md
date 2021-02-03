# refresh_ahv

Refresh the metadata for the specified Nutanix AHV cluster.

```py
def refresh_ahv(self, nutanix_ahv_cluster, wait_for_completion=True, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| nutanix_ahv_cluster | str | The name of the AHV cluster you wish to refresh. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| wait_for_completion  | bool | Flag to determine if the function should wait for the refresh to complete before completing.  |  | True |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | When wait_for_completion is False, the full API response for `POST /internal/nutanix/cluster/{id}/refresh` |
| dict | When wait_for_completion is True, the full API response of the job status |



## Example

```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()

nutanix_ahv_hostname = "ahvcluster"
refresh_ahv = rubrik.refresh_ahv(nutanix_ahv_hostname)
print(refresh_ahv)

```
