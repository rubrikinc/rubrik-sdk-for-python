# submit_restore_gce

Submits a Restore of a GCE instance

```py
def submit_restore_gce(self, snapshot_id, **kwargs):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| snapshot_id  | str | Snapshot ID to be restored |  |
| should_power_on  | bool | Defaults to `False` |  |
| should_restore_tags  | bool | Defaults to `False` |  |
| wait  | bool | Return once complete Defaults to `False` |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of errors if any occured during the restore |



