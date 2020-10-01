# get\_esxi\_subnets

Retrieve the preferred subnets used to reach the ESXi hosts.

```python
def get_esxi_subnets(self, timeout=15):
```

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `GET /internal/vmware/config/esx_subnets`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

rubrik.get_esxi_subnets()
```

