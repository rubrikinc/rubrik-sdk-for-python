# aws_s3_cloudon

Enable CloudOn for an exsiting AWS S3 archival location.

```py
def aws_s3_cloudon(self, archive_name, vpc_id, subnet_id, security_group_id, enable_archive_consolidation=False, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| archive_name  | str | The name of the archive location used in the Rubrik GUI. |  |
| vpc_id  | str | The AWS VPC ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |  |
| subnet_id  | str | The AWS Subnet ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |  |
| security_group_id  | str | The AWS Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| enable_archive_consolidation  | bool |  - Flag that determines whether archive consolidation is enabled.  |  | False |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The '`name`' archival location is already configured on the Rubrik cluster. |
| dict | The full API response for `PATCH /internal/archive/object_store/{id}`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

archive_name = "AWS:S3:rubrikpythonsdk"
vpc_id = 'vpc-8d80iii9'
subnet_id = 'subnet-125b5q79'
security_group_id = 'sg-f31bb489'
enable_archive_consolidation = True

cloudon = rubrik.aws_s3_cloudon(archive_name, vpc_id, subnet_id, security_group_id, enable_archive_consolidation)

```
