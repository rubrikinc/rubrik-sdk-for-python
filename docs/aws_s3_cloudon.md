# aws_s3_cloudon

Enable CloudOn for an exsiting AWS S3 archival location.
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
| vpc_id  | str  | The AWS VPC ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |         |         |
| subnet_id  | str  | The AWS Subnet ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |         |         |
| security_group_id  | str  | The AWS Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in AWS for instantiation. |         |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`name`' archival location is already configured on the Rubrik cluster. |
| dict  | The full API response for `PATCH /internal/archive/object_store/{id}`. |
## Example
```py
import rubrik

rubrik = rubrik.Connect()

with open("/home/python-sdk-demo/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

archive_name = "AWS:S3:rubrikpythonsdk"
vpc_id = 'vpc-8d80iii9'
subnet_id = 'subnet-125b5q79'
security_group_id = 'sg-f31bb489'

cloudon = rubrik.aws_s3_cloudon(archive_name, vpc_id, subnet_id, security_group_id)
```