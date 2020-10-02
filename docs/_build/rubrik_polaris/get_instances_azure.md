# get_instances_azure

Retrieve all Azure instances from Polaris

```py
def get_instances_azure(self):
```



## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all Azure VM instances |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

# Search for a set of objects and get their details
for i in client.get_object_ids_azure():
    print(client.get_instances_azure(i))

```
