# add_organization_protectable_object_mssql_server_host

Add a MSSQL Server Host to an organization as a protectable object.

```py
def add_organization_protectable_object_mssql_server_host(self, organization_name, mssql_host, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| organization_name  | str | The name of the organization you wish to add the protectable object to. |  |
| mssql_host  | str | The name of the MSSQL Host to add to the organization as a protectable object. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The MSSQL host {mssql_host} is already assigned to the {organization_name} organization. |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
mssql_host = "demo.rubrikdemo.com"

update_org = rubrik.add_organization_protectable_object_mssql_server_host(org, mssql_host)
```
