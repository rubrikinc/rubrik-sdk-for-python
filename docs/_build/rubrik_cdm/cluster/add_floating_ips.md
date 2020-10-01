# add\_floating\_ips

Add floating IPs to CDM.

```python
def add_floating_ips(self, floating_ips, wait_for_completion=True, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| floating\_ips | list | The IP addresses you wish to add. |  |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | When wait\_for\_completion is False, the full API response for `POST /internal/node_management/cluster_ip` |
| dict | When wait\_for\_completion is True, the full API response of the job status |

