# object_id

Get the ID of a Rubrik object by providing its name.
```py
def object_id(object_name, object_type)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str  | The name of the Rubrik object whose ID you wish to lookup. |         |
| object_type  | str  | The object type you wish to look up.  |    vmware, sla, vmware_host     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | The ID of the provided Rubrik object. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

vmware_id = rubrik.object_id(vm_name, object_type)
```