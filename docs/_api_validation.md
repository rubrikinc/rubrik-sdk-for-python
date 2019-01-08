# _api_validation

Internal method used to validate the API Version and API Endpoint provided by the end user
```py
def _api_validation(api_version, api_endpoint)
```

## Arguments
| Name         | Type | Description                                                   | Choices          |
|--------------|------|---------------------------------------------------------------|------------------|
| api_version  | str  | The version of the Rubrik CDM API to call.                    | v1, v2, internal |
| api_endpoint | str  | The endpoint of the Rubrik CDM API to call (ex. /cluster/me). |                  |
