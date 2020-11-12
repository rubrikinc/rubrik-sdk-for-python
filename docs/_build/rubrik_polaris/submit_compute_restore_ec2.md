# submit_compute_restore_ec2

Submits a Restore of an EC2 instance

```py
def submit_compute_restore_ec2(self, snapshot_id, **kwargs):
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



