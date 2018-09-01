# azure_cloudon

Add a new Azure archival location to the Rubrik cluster and optionally configure the required Cloud On options.
```py
def azure_cloudon(archive_name, container, storage_account_name, application_id, application_key, tenant_id, region, virtual_network_id, subnet_name, security_group_id, timeout=30)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| archive_name  | str  | The name of the archive location used in the Rubrik GUI. |         |
| container  | str  | The name of the Azure storage container you wish to use as an archive. The container name will automatically be lowercased and can not contain any of the following characters: `_\/*?%.:|<>` |         |
| storage_account_name  | str  | The name of the Storage Account that the `container` belongs to. |         |
| application_id  | str  | The ID of the application registered in Azure Active Directory. Only required when configuring Cloud On. |         |
| application_key  | str  | The key of the application registered in Azure Active Directory. Only required when configuring Cloud On. |         |
| tenant_id  | str  | The tenant ID, also known as the directory ID found under the Azure Active Directory properties. Only required when configuring Cloud On. |         |
| region  | str  | The name of the Azure region where the `container` is located. Only required when configuring Cloud On. (choices: {"westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"}) |    "westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"     |
| virtual_network_id  | str  | The virtual network ID used for Cloud On. |         |
| subnet_name  | str  | The subnet name used for Cloud On. |         |
| security_group_id  | str  | The security group ID used for Cloud On. |         |
| timeout  | int  | The timeout value for the API call that configures the CloudOn instantiation configs. (default: {30}) |         |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`archive_name`' archival location is already configured for CloudOn. |
| dict  | The full API response for `PATCH /internal/archive/object_store/{id}`. |
