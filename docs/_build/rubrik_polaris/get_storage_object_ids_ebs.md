# get_storage_object_ids_ebs

Retrieves all AWS EBS object IDs that match query

```py
def get_storage_object_ids_ebs(self, match_all=True, **kwargs):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| match_all  | bool | Set to False to match ANY defined criteria |  |
| tags  | name: value | Allows simple qualification of tags |  |
| kwargs  |  | Any top level object from the get_storage_ebs call |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all the EBS object id's |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

print(client.get_storage_object_ids_ebs(tags = {"Class": "Management"}))

```
