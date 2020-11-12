# submit_on_demand

Submits On Demand Snapshot request for the given set of object id's and assign the given SLA to the snapshots.

```py
def submit_on_demand(self, object_ids, sla_id, wait=False):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_ids  | [str] | Array of Rubrik Object IDs |  |
| sla_id  | str | Rubrik SLA Domain ID |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| wait  | bool | Threaded wait for all processes to complete  |  | False |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of errors if any occurred |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'

client = PolarisClient(domain, username, password, insecure=True)


# Run On-Demand Snapshot for machines in us_west1 using Gold retention, wait until completion

object_ids = client.get_object_ids_gce(region='us-west-1')
sla_domain_id = client.get_sla_domains('Gold')[0]['id']

client.submit_on_demand(object_ids, sla_domain_id, wait=True)

```
