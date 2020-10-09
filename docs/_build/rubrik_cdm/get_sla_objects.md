# get_sla_objects

Retrieve the name and ID of a specific object type.

```py
def get_sla_objects(self, sla, object_type, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| sla  | str | The name of the SLA Domain you wish to search. |  |
| object_type  | str | The object type you wish to search the SLA for.  | vmware, hyper-v, mssql_db, ec2_instance, oracle_db, vcd, managed_volume, ahv, nas_share, linux_and_unix_host, windows_host |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The `name:id` of each object in the provided SLA Domain. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vms_in_sla = rubrik.get_sla_objects("Gold", "vmware")

```
