# add_account_aws

Adds AWS account to Polaris

```py
def add_account_aws(self, account_id, account_name, regions):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| account_id  | str | AWS account id to add |  |
| account_name  | str | Friendly name for account in Polaris |  |
| regions  | list | List of AWS regions to configure |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| int | 1 if the account was added successfully |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '339701109484'


client = PolarisClient(domain, username, password, insecure=True)
client.add_account_aws(aws_account_id, 'my-aws-account', ['us-east-1'])

```
