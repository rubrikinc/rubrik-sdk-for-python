# get\_sla\_objects

Retrieve the name and ID of a specific object type.

```python
def get_sla_objects(self, sla, object_type, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| sla | str | The name of the SLA Domain you wish to search. |  |
| object\_type | str | The object type you wish to search the SLA for. | vmware, hyper-v, mssql\_db, ec2\_instance, oracle\_db, vcd, managed\_volume, ahv, nas\_share, linux\_and\_unix\_host, windows\_host |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The `name:id` of each object in the provided SLA Domain. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vms_in_sla = rubrik.get_sla_objects("Gold", "vmware")
```

