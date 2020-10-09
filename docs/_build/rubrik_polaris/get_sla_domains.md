# get_sla_domains

Retrieves dictionary of SLA Domain Names and Identifiers, or the ID of a single SLA Domain

```py
def get_sla_domains(self, sla_domain_name=""):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| sla_domain_name  | str | Rubrik SLA Domain name |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | ID for the given SLA Domain name as given by `sla_domain_name` |
| dict | If a `sla_domain_name` is not given or not found, the complete set of SLA domains will be returned |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

client = PolarisClient(domain, username, password, insecure=True)
sla_domains = client.get_sla_domains()

```
