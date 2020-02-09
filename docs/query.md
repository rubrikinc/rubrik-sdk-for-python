# query

Send a GraphQL query to CDM cluster.
```py
def query(self, query, operation_name=None, variables=None, timeout=15,authentication=True):

```

## Arguments
| Name           | Type | Description                                                                                                                               | Choices | Default |   |
|----------------|------|-------------------------------------------------------------------------------------------------------------------------------------------|---------|---------|---|
| query          | str  | The main GraphQL query body.                                                                                                              |         |         |   |
| operation_name | str  | A meaningful and explicit name for your GraphQL operation. Think of this just like a function name in your favorite programming language. |         | None    |   |
| variables      | dict | The variables to pass into your query.                                                                                                    |         | None    |   |

## Keyword Arguments
| Name           | Type | Description                                                                                                  | Choices | Default |
|----------------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| timeout        | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 15      |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call.                       |         | True    |

## Returns
| Type | Return Value                       |
|------|------------------------------------|
| dict | The response["data"] body of the API call.  |

## Example

# Query Only

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

query = """
{
  cluster(id: "me") {
    version
  }
}
"""

cluster_details = rubrik.query(query)
```

# All parameters used

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

operation_name = "ClusterDetails"

query = """
ClusterDetails($clusterID: String!) {
  cluster(id: $clusterID) {
    version
  }
}
"""

variables = {
    "clusterID": "me"
}

cluster_details = rubrik.query(query, operation_name, variables)
```




