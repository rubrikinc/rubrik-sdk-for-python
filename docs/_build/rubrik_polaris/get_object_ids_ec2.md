# get_object_ids_ec2

Retrieves all AWS EC2 object IDs that match query

```py
def get_object_ids_ec2(self, match_all=True, **kwargs):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| match_all  | bool | Set to false to match ANY defined criteria |  |
| tags  | name: value | Allows simple qualification of tags |  |
| kwargs  |  | Any top level object from the get_instances_ec2 call |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all the EC2 object id's |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

# Search for a set of objects and get their details
for i in client.get_object_ids_ec2(region = 'US_WEST_2'):
    print(client.get_instances_ec2(i))

```
