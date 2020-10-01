# set\_esxi\_subnets

Sets the subnets that should be used to reach the ESXi hosts.

```python
def set_esxi_subnets(self, esx_subnets=None, timeout=15):
```

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| esx\_subnets | list | Preferred subnets used to reach the ESX hosts. |  |  |
| timeout | int | The number of seconds to wait to establish a connection with the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `PATCH /internal/vmware/config/set_esx_subnets`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

subnets = rubrik.set_esxi_subnets(["192.168.2.10/24","10.255.0.2/16"])
```

