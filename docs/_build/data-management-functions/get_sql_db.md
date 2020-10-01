# get\_sql\_db

Retrieves summary information for SQL databases. Each keyword argument is a query parameter to filter the database details returned i.e. you can query for a specific database name, hostname, instance, is\_relic, effective\_sla\_domain etc.

```python
def get_sql_db(self, db_name=None, instance=None, hostname=None, availability_group=None, effective_sla_domain=None, primary_cluster_id='local', sla_assignment=None, limit=None, offset=None, is_relic=None, is_live_mount=None, is_log_shipping_secondary=None, sort_by=None, sort_order=None, timeout=15):
```

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| db\_name | str | Filter by a substring of the database name. |  |  |
| instance | str | The SQL instance name of the database. |  |  |
| hostname | str | The SQL host name of the database. |  |  |
| availability\_group | str | Filter by the name of the Always On Availability Group. |  |  |
| effective\_sla\_domain | str | Filter by the name of the effective SLA Domain. |  |  |
| primary\_cluster\_id | str | Filter by primary cluster ID, or local. |  |  |
| sla\_assignment | str | Filter by SLA Domain assignment type. \(Direct, Derived, Unassigned\) |  |  |
| limit | int | Limit the number of matches returned. |  |  |
| offset | int | Ignore these many matches in the beginning. |  |  |
| is\_relic | bool | Filter database summary information by the value of the isRelic field. |  |  |
| is\_live\_mount | bool | Filter database summary information by the value of the isLiveMount field. |  |  |
| is\_log\_shipping\_secondary | bool | Filter database summary information by the value of the isLogShippingSecondary field. |  |  |
| sort\_by | str | Sort results based on the specified attribute. \(effectiveSlaDomainName, name\) |  |  |
| sort\_order | str | Sort order, either ascending or descending. \(asc, desc\) |  |  |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The full response of `GET /v1/mssql/db?{query}` |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "python-sdk-demo"
instance = 'MSSQLSERVER'
hostname = 'sql.rubrikdemo.com'
availability_group = 'sql.rubrikdemo.com'
effective_sla_domain = 'Gold'
primary_cluster_id = 'local'
sla_assignment = 'Direct'

get_db = rubrik.get_sql_db(db_name=db_name, instance=instance, hostname=hostname, availability_group=availability_group, effective_sla_domain=effective_sla_domain, primary_cluster_id=primary_cluster_id, sla_assignment=sla_assignment)
```

