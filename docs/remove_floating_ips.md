# remove_floating_ips

Remove floating IPs from CDM.

```py
def remove_floating_ips(self, floating_ips, wait_for_completion=True, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| floating_ips  | list | The IP addresses you wish to remove. |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | When wait_for_completion is False, the full API response for `POST /internal/node_management/cluster_ip` |

