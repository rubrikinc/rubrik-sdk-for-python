# object_id

Get the ID of a provided object (ex. VM, SLA, etc.) by providing its name.

```py
def object_id(object_name, object_type=None)
```

## Arguments
object_name {str} -- The name of the object whose ID you wish to lookup.


## Keyword Arguments
object_type {str} -- The object type you wish to look up. Valid options are vmware and sla. (default: {None})


## Returns
[str] -- The ID of the provided object.



