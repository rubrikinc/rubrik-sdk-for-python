# cluster_search_domain

Configure the DNS search domains on the Rubrik cluster.
```py
def cluster_search_domain(search_domain, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| search_domain  | list  | The DNS search domains you wish to add to the Rubrik cluster. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster is already configured with the provided DNS search domains. |
| dict  | The full API response for `POST /internal/cluster/me/dns_search_domain'` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

search_domains = ["python.lab", "go.lab"]
cluster_search_domains = rubrik.cluster_search_domain(search_domains)
```