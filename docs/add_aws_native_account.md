# add_aws_native_account

Add a new AWS account to EC2 native protection on the Rubrik cluster.
```py
def add_aws_native_account(aws_account_name, aws_access_key=None, aws_secret_key=None, aws_regions=None, regional_bolt_network_configs=None, timeout=30)
```

## Arguments
| Name             | Type | Description                                                                                                | Choices |
|------------------|------|------------------------------------------------------------------------------------------------------------|---------|
| aws_account_name | str  | The name of the AWS account you wish to protect. This is the name that will be displayed in the Rubrik UI. |         |
## Keyword Arguments
| Name                          | Type          | Description                                                                                                                                                                                           | Choices                                                                                                                                                                                                                         | Default |
|-------------------------------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| aws_access_key                | str           | The access key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_ACCESS_KEY_ID` environment variable to pull the value from.     |                                                                                                                                                                                                                                 | None    |
| aws_secret_key                | str           | The secret key of a AWS account with the required permissions. If set to the default `None` keyword argument, we will look for a `AWS_SECRET_ACCESS_KEY` environment variable to pull the value from. |                                                                                                                                                                                                                                 | None    |
| aws_regions                   | list          | List of AWS regions to protect in this AWS account. If set to the default `None` keyword argument, we will look for a `AWS_DEFAULT_REGION` environment variable to pull the value from.               | ap-south-1, ap-northeast-3, ap-northeast-2, ap-southeast-1, ap-southeast-2, ap-northeast-1, ca-central-1, cn-north-1, cn-northwest-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, us-west-1, us-east-1, us-east-2, us-west-2 | None    |
| regional_bolt_network_configs | list of dicts | List of dicts containing per region bolt network configs. (ex. dict format: {"region": "aws-region-name", "vNetId": "aws-vpc-id", "subnetId": "aws-subnet-id", "securityGroupId": "aws-subnet-id"})   |                                                                                                                                                                                                                                 | None    |
| timeout                       | int           | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.                                                                                          |                                                                                                                                                                                                                                 | 30      |

## Returns
| Type | Return Value                                                                                                          |
|------|-----------------------------------------------------------------------------------------------------------------------|
| str  | No change required. Cloud native source with access key `aws_access_key` is already configured on the Rubrik cluster. |
| dict | The full API response for `POST /internal/aws/account'`.                                                              |
## Example
```py
import rubrik_cdm
rubrik = rubrik_cdm.Connect()

name = 'pythonsdkdemo'
accessKey = 'AWS_ACCESS_KEY'
secretKey = 'AWS_SECRET_KEY'
regions = ['us-east-1']
regional_bolt_network_configs = [
    {
        "region": "us-east-1",
        "vNetId": "vpc-a46e72c2",
        "subnetId": "subnet-f0cc9695",
        "securityGroupId": "sg-66091b19"
    }
]

nativeaccount = rubrik.add_aws_native_account(name, accessKey, secretKey, regions, regional_bolt_network_configs)
```