# post()

Connect to a Rubrik Cluster and perform a POST operation.

## Arguments
api_version {str} -- The version of the Rubrik CDM API to call.

api_endpoint {str} -- The endpoint (ex. cluster/me) of the Rubrik CDM API to call.

config {dict} -- The specified data to send with the API call.


## Keyword Arguments
timeout {int} -- The number of seconds to wait to establish a connection the Rubrik Cluster. (default: {15})

authentication {bool} -- Flag that specifies whether or not to utilize authentication when making the API call. (default: {True})


## Returns
dict -- The response body of the API call.



