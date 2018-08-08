# delete

Send a DELETE request to the provided Rubrik API endpoint.

```py
def delete(api_version, api_endpoint, timeout=15, authentication=True)
```

## Arguments
api_version {str} -- The version of the Rubrik CDM API to call.

api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.


## Keyword Arguments
timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15})

authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})


## Returns
dict -- The response body of the API call.



