# get_storage_ebs

Retrieve all AWS EBS volumes from Polaris

```py
def get_storage_ebs(self):
```



## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all the AWS EBS volumes. |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

print(client.get_storage_ebs())

```
