# add_aws_s3_archive

Add a new AWS S3 archive target to the Rubrik Cluster and optionally configure the required Cloud On options.
```py
def add_aws_s3_archive(aws_bucket_name, aws_region=None, aws_access_key=None, aws_secret_key=None, kms_master_key_id=None, rsa_key=None, name='default', storage_class='standard', vpc_id=None, subnet_id=None, security_group_id=None)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| aws_bucket_name  | str  | The name of the AWS S3 bucket you wish to use. The bucket name will automatically have all whitespace removed and all letters will be lowercased. The bucket name may not contain any of the following characters: `_\/*?%.:|<>` |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| aws_region  | str  | The name of the AWS region where the bucket is located. If set to the default `None` value we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from. (default: {None}) (choices: {'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1' 'us-west-1' 'us-east-1', 'us-east-2', 'us-west-2'}) |    'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1' 'us-west-1' 'us-east-1', 'us-east-2', 'us-west-2'     |    None (choices: {'ap-south-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'cn-north-1', 'cn-northwest-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'sa-east-1', 'us-gov-west-1' 'us-west-1' 'us-east-1', 'us-east-2', 'us-west-2'     |
| aws_access_key  | str  | The access key of account with the required permissions. If set to the default `None` value we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from. (default: {None}) |         |    None     |
| aws_secret_key  | str  | The secret key of account with the required permissions. If set to the default `None` value we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from. (default: {None}) |         |    None     |
| kms_master_key_id  | str  | The AWS master key Id that will be used to encrypt the archive data. If set to the default `None` value you will need to provide a `rsa_key` instead. (default: {None}) |         |    None     |
| rsa_key  | str  | The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. If set to the default `None` value you will need to provide a `kms_master_key_id` instead.  (default: {None}) |         |    None     |
| name  | str  | The name of the archive location used in the Rubrik GUI. If set to default the following naming convention will be used: AWS:S3:{`aws_bucket_name`} (default: {'default'}) |         |    'default'     |
| storage_class  | str  | The storage class you wish to use. (default: {'standard'}) (choices: {'standard', 'standard_ia', 'reduced_redundancy'}) |    'standard', 'standard_ia', 'reduced_redundancy'     |    'standard' (choices: {'standard', 'standard_ia', 'reduced_redundancy'     |
| vpc_id  | str  | The VPC Id used for Cloud On. When a value has been provided you must also provide a value for `subnet_id` and `security_group_id` (default: {None}) |         |    None     |
| subnet_id  | str  | The Subnet id used for Cloud On. When a value has been provided you must also provide a value for `vpc_id` and `security_group_id` (default: {None}) |         |    None     |
| security_group_id  | str  | The Security Group Id used for Cloud On. When a value has been provided you must also provide a value for `vpc_id` and `subnet_id` (default: {None}) |         |    None     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '{`name`}' Archival location is already configured on the Rubrik Cluster. |
| dict  | The full API response for `POST /internal/archive/object_store'. |
