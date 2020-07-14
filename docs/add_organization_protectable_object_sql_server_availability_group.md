# add_organization_protectable_object_sql_server_availability_group

Add a MSSQL Availability Group to an organization as a protectable object.

```py
def add_organization_protectable_object_sql_server_availability_group(self, organization_name, mssql_availability_group, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| organization_name  | str | The name of the organization you wish to add the protectable object to. |  |
| mssql_availability_group  | str | The name of the MSSQL Availability Group to add to the organization as a protectable object. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The MSSQL Availability Group {mssql_availability_group} is already assigned to the {organization_name} organization. |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
ag = "demo-ag"

update_org = rubrik.add_organization_protectable_object_sql_server_availability_group(org, ag)
```
