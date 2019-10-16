# get_vsphere_vm

Get summary of all the VMs. Each keyword argument is a query parameter to filter the VM details returned i.e. you can query for a specific VM name, is_relic, effective_sla_domain etc.
```py
def get_vsphere_vm(name=None, is_relic=None, effective_sla_domain_id=None, primary_cluster_id=None, limit=None, offset=None, moid=None, sla_assignment=None, guest_os_name=None, sort_by=None, sort_order=None, timeout=15)
```

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| name  | str  | Search by using a virtual machine name.  |         |         |
| is_relic  | bool  | Filter by the isRelic field of the virtual machine. When this parameter is not set, return both relic and non-relic virtual machines. |         |         |
| effective_sla_domain_id  | str  | Filter by ID of effective SLA Domain.  |         |         |
| primary_cluster_id  | str  | Filter by primary cluster ID, or local.  |         |         |
| limit  | int  | Limit the number of matches returned.  |         |         |
| offset  | int  | Ignore these many matches in the beginning.  |         |         |
| moid  | str  | Search by using a virtual machine managed object ID.  |         |         |
| sla_assignment  | str  | Filter by SLA Domain assignment type.   |     Direct, Derived, Unassigned    |         |
| guest_os_name  | str  | Filters by the name of operating system using infix search.  |         |         |
| sort_by  | str  | Sort results based on the specified attribute.  |     effectiveSlaDomainName, name, moid, folderPath, infraPath    |         |
| sort_order  | str  | Sort order, either ascending or descending.   |    asc, desc    |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| dict  | The full response of `GET /v1/vmware/vm?{query}`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"

get_vm = rubrik.get_vsphere_vm(name=vm_name)
```