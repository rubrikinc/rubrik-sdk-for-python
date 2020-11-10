# get_sla_domains

Retrieves dictionary of SLA Domain Names and Identifiers.

```py
def get_sla_domains(self, sla_domain_name=""):
```


## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sla_domain_name  | str | Rubrik SLA Domain name  |  |  |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | ID for the given SLA Domain name as given by `sla_domain_name` |
| dict | The complete set of SLA domains or a one element dict if a non-empty `sla_domain_name` is given and found. |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

client = PolarisClient(domain, username, password, insecure=True)
sla_domains = client.get_sla_domains()

```
