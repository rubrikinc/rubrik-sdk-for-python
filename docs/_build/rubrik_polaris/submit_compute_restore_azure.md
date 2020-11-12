# submit_compute_restore_azure

Submits a Restore of an Azure VM instance

```py
def submit_compute_restore_azure(self, snapshot_id, **kwargs):
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
| list | List of errors if any occurred during the restore |



