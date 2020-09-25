# submit_restore_ec2

Submits a Restore of an EC2 instance

```py
def submit_restore_ec2(self, snapshot_id, **kwargs):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| snapshot_id  | string | Snapshot ID to be restored |  |
| should_power_on  | bool | Defaults to False |  |
| should_restore_tags  | bool | Defaults to False |  |
| wait  | bool | Return once complete Defaults to False |  |





