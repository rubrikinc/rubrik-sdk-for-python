# submit\_restore\_ec2

Submits a Restore of an EC2 instance

```python
def submit_restore_ec2(self, snapshot_id, **kwargs):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| snapshot\_id | string | Snapshot ID to be restored |  |
| should\_power\_on | bool | Defaults to False |  |
| should\_restore\_tags | bool | Defaults to False |  |
| wait | bool | Return once complete Defaults to False |  |

