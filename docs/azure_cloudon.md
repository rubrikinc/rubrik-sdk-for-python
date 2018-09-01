# azure_cloudon

Enable CloudOn for an exsiting AWS S3 archival location.
```py
def azure_cloudon(archive_name, container, storage_account_name, application_id, application_key, tenant_id, region, virtual_network_id, subnet_name, security_group_id, timeout=30)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| archive_name  | str  | The name of the archive location used in the Rubrik GUI. |         |
| container  | str  | The name of the Azure storage container being used as the archive target. The container name will automatically be lowercased and can not contain any of the following characters: `_\/*?%.:|<>` |         |
| storage_account_name  | str  | The name of the Storage Account that the `container` belongs to. |         |
| application_id  | str  | The ID of the application registered in Azure Active Directory. |         |
| application_key  | str  | The key of the application registered in Azure Active Directory. |         |
| tenant_id  | str  | The tenant ID, also known as the directory ID, found under the Azure Active Directory properties. |         |
| region  | str  | The name of the Azure region where the `container` is located.  |    westus, westus2, centralus, eastus, eastus2, northcentralus, southcentralus, westcentralus, canadacentral, canadaeast, brazilsouth, northeurope, westeurope, uksouth, ukwest, eastasia, southeastasia, japaneast, japanwest, australiaeast australiasoutheast, centralindia, southindia, westindia, koreacentral, koreasouth     |
| virtual_network_id  | str  | The Azure virtual network ID used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation. |         |
| subnet_name  | str  | The Azure subnet name used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation. |         |
| security_group_id  | str  | The Azure Security Group ID used by Rubrik cluster to launch a temporary Rubrik instance in Azure for instantiation. |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {30}) |         |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`archive_name`' archival location is already configured for CloudOn. |
| dict  | The full API response for `PATCH /internal/archive/object_store/{id}`. |
