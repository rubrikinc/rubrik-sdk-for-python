# get_snapshots

Retrieve Snapshots for a Snappable from Polaris

```py
def get_snapshots(self, snappable_id, **kwargs):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| snappable_id  | str | Object UUID |  |
| recovery_point  | str | Optional datetime of snapshot to return, or 'latest', or not defined to return all |  |


## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | A dictionary of snapshots or a single snapshot if 'latest' was passed as `recovery_point`. If no snapshots are found, an empty dict is returned. |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

snappables = client.get_object_ids_ec2(tags={"Environment": "staging"})
for snappable in snappables:
    snapshot = client.get_snapshots(snappable, recovery_point='latest')
    if snapshot:
        print(snapshot[0])

```
