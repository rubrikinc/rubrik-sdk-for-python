# aws_s3_cloudon

Configure the CloudOn instantiation configs on an exsiting AWS S3 archival location.
```py
def aws_s3_cloudon(archive_name, vpc_id, subnet_id, security_group_id, timeout=30)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| archive_name  | str  | The name of the archive location used in the Rubrik GUI. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| vpc_id  | str  | The VPC ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. When a value has been provided you must also provide a value for `subnet_id` and `security_group_id` (default: {None}) |         |    None     |
| subnet_id  | str  | The Subnet ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. When a value has been provided you must also provide a value for `vpc_id` and `security_group_id` (default: {None}) |         |    None     |
| security_group_id  | str  | The Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. When a value has been provided you must also provide a value for `vpc_id` and `subnet_id` (default: {None}) |         |    None     |
| timeout  | int  | The timeout value for the API call that configures the CloudOn instantiation configs. (default: {30}) |         |    30     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`name`' archival location is already configured on the Rubrik cluster. |
| dict  | The full API response for `PATCH /internal/archive/object_store/{id}`. |
