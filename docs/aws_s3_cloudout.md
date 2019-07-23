# aws_s3_cloudout

Add a new AWS S3 archival location to the Rubrik cluster.
```py
def aws_s3_cloudout(aws_bucket_name, archive_name='default', aws_region=None, aws_access_key=None, aws_secret_key=None, kms_master_key_id=None, rsa_key=None, storage_class='standard', timeout=180)
```

## Arguments
| Name            | Type | Description                                                                                                                                                                                                                 | Choices |
|-----------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| aws_bucket_name | str  | The name of the AWS S3 bucket you wish to use as an archive target. The bucket name will automatically have all whitespace removed, all letters lowercased, and can not contain any of the following characters: `_\/*?%.:\ | <>`.    |
## Keyword Arguments
| Name              | Type | Description                                                                                                                                                                                                                                            | Choices                                                                                                                                                                                                                                   | Default  |
|-------------------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| aws_region        | str  | The name of the AWS region where the bucket is located. If set to the default `None` keyword argument, we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from.                                                            | ap-south-1, ap-northeast-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, ca-central-1, cn-north-1, cn-northwest-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, sa-east-1, us-gov-west-1, us-west-1, us-east-1, us-east-2, us-west-2 | None     |
| aws_access_key    | str  | The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from.                                                      |                                                                                                                                                                                                                                           | None     |
| aws_secret_key    | str  | The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from.                                                  |                                                                                                                                                                                                                                           | None     |
| kms_master_key_id | str  | The AWS KMS master key ID that will be used to encrypt the archive data. If set to the default `None` keyword argument, you will need to provide a `rsa_key` instead.                                                                                  |                                                                                                                                                                                                                                           | None     |
| rsa_key           | str  | The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. If set to the default `None` keyword argument, you will need to provide a `kms_master_key_id` instead. |                                                                                                                                                                                                                                           | None     |
| archive_name      | str  | The name of the archive location used in the Rubrik GUI. If set to 'default' the following naming convention will be used: "AWS:S3:`aws_bucket_name`"                                                                                                  |                                                                                                                                                                                                                                           | default  |
| storage_class     | str  | The AWS storage class you wish to use.                                                                                                                                                                                                                 | standard, standard_ia, reduced_redundancy                                                                                                                                                                                                 | standard |
| timeout           | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                                                                                                           |                                                                                                                                                                                                                                           | 180      |

## Returns

| Type | Return Value                                                                                    |
|------|-------------------------------------------------------------------------------------------------|
| str  | No change required. The '`name`' archival location is already configured on the Rubrik cluster. |
| dict | The full API response for `POST /internal/archive/object_store`.                                |

## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

with open("/home/python-sdk-demo/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

aws_bucket_name = 'rubrikpythonsdk'

# AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY are being read from environment variables
cloudout = rubrik.aws_s3_cloudout(aws_bucket_name, rsa_key=rsa_key)
```