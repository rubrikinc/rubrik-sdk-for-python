# add_account_aws

Adds AWS account to Polaris

```py
def add_account_aws(self, regions=[], all=False, profiles=[], aws_access_key_id=None, aws_secret_access_key=None):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| regions  | list | List of AWS regions to configure |  |
| all  | bool | If true import all available profiles (Default: False) |  |
| profiles  | list | List of explicit profiles to add |  |
| aws_access_key_id  | str | AWS Access Key ID |  |
| aws_secret_access_key  | str | AWS Access Key Secret |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| bool | `True` if the account was added successfully, otherwise `False`. |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)
success = client.add_account_aws(regions=["us-west-2"], all=True)
if success:
    print("AWS Account added successfully!")

```
