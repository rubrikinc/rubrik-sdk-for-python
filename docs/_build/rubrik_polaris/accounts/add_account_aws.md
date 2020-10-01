# add\_account\_aws

Adds AWS account to Polaris

```python
def add_account_aws(self, _account_id, _account_name, _regions):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| \_account\_id | string | AWS account id to add |  |
| \_account\_name | str | Friendly name for account in Polaris |  |
| \_regions | list | List of AWS regions to configure |  |

## Example

```python
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '789702809484'


client = PolarisClient(domain, username, password, insecure=True)
client.add_account_aws(aws_account_id, 'my-aws-account', ['us-east-1'])
```

