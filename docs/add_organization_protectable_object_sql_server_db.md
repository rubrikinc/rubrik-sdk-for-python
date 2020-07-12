# add_organization_protectable_object_sql_server_db

Add a MSSQL Database to an organization as a protectable object.

```py
def add_organization_protectable_object_sql_server_db(self, organization_name, mssql_db, mssql_host, mssql_instance, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| organization_name  | str | The name of the organization you wish to add the protectable object to. |  |
| mssql_db  | str | The name of the MSSQL DB to add to the organization as a protectable object. |  |
| mssql_instance  | str | The name of the MSSQL Instance where the DB lives. |  |
| mssql_host  | str | The name of the MSSQL Host where the DB lives. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The MSSQL DB {mssql_db} is already assigned to the {organization_name} organization. |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

org = "PythonSDK"
mssql_db = "DemoData"
mssql_host = "demo.rubrikdemo.com"
mssql_instance = "DEMOINSTANCE"

update_org = rubrik.add_organization_protectable_object_sql_server_db(org, mssql_db, mssql_host, mssql_instance)

```
