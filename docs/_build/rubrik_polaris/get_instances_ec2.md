# get_instances_ec2

Retrieve all AWS EC2 instances from Polaris

```py
def get_instances_ec2(self, object_id=None):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_id  | str | A specific Object ID to retrieve |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all the AWS EC2 instances or the specific instance if the `object_id` is passed. |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

aws_account_id = '789702809484'


client = PolarisClient(domain, username, password, insecure=True)

# Search for a set of objects and get their details
for i in client.get_object_ids_ec2(region = 'US_WEST_2'):
    print(client.get_instances_ec2(i))

```
