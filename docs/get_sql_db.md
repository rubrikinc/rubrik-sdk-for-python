# get_sql_db

""" Retrieves summary information for Microsoft SQL databases. Each keyword argument is a query parameter to filter the database details returned i.e. you can query for a specific database name, hostname, instance, is_relic, effective_sla_domain etc.
```py
def get_sql_db(instance_id=None, availability_group_id=None, effective_sla_domain_id=None, primary_cluster_id=None, name=None, instance=None, hostname=None, sla_assignment=None, limit=None, offset=None,  is_relic=None, is_live_mount=None, is_log_shipping_secondary=None, sort_by=None, sort_order=None, timeout=15)
```

## Keyword Arguments
| Name                      | Type | Description                                                                 | Choices | Default |
|---------------------------|------|-----------------------------------------------------------------------------|---------|---------|
| name                      | str  | Filter by a substring of the database name.                                 |         |         |
| instance                  | str  | The SQL instance name of the database.                                      |         |         |
| hostname                  | str  | The SQL host name of the database.                                          |         |         |
| instance_id               | str  | Filter by Microsoft SQL instance.                                           |         |         |
| availability_group_id     | str  | Filter by the id of an Always On Availability Group.                        |         |         |
| effective_sla_domain_id   | str  | Filter by ID of effective SLA Domain.                                       |         |         |
| primary_cluster_id        | str  | Filter by primary cluster ID, or local.                                     |         |         |
| sla_assignment            | str  | Filter by SLA Domain assignment type.                                       |Direct, Derived, Unassigned |         |
| limit                     | int  | Limit the number of matches returned.                                       |         |         |
| offset                    | int  | Ignore these many matches in the beginning.                                 |         |         |
| is_relic                  | bool | Filter by the isRelic field of the database.                                |         |         |
| is_live_mount             | bool | Filter database summary information by the value of the isLiveMount field.  |         |         |
| is_log_shipping_secondary | bool | Filter database summary information by the value of the isLogShippingSecondary field.|         |         |
| sort_by                   | str  | Sort results based on the specified attribute.                              | effectiveSlaDomainName, name |         |
| sort_order                | str  | Sort order, either ascending or descending.                                 | asc, desc |         |
| timeout                   | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         |    15     |

## Returns
| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full response of `GET /v1/mssql/db?{query}`.                                              |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

name = "python-sdk-demo"
instance = 'MSSQLSERVER'
hostname = 'sql.rubrikdemo.com'

get_db = rubrik.get_sql_db(name=name, instance=instance, hostname=hostname)
```