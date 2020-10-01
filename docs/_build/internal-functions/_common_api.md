# \_common\_api

Internal method that consolidates the base API functions.

```python
def _common_api(self, call_type, api_version, api_endpoint, config=None, job_status_url=None, timeout=15, authentication=True, params=None, gql_operation_name=None, gql_query=None, gql_variables=None):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| call\_type | str | The HTTP Method for the type of RESTful API call being made. | 'GET', 'POST', 'PATCH', 'DELETE', and 'JOB\_STATUS'. |
| api\_version | str | The version of the Rubrik CDM API to call. | v1, v2, internal |
| api\_endpoint | str | The endpoint of the Rubrik CDM API to call \(ex. /cluster/me\). |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| params | dict | An optional dict containing variables in a key:value format to send with `GET` & `DELETE` API calls |  | None |
| config | dict | The specified data to send with 'DELETE', `POST` and `PATCH` API calls. |  | None |
| job\_status\_url | str | The job status URL provided by a previous API call. |  | None |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call. |  | True |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full API call response for the provided endpoint. |

