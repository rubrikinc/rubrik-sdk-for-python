# add_archive_azure

Add a new Azure archive target to the Rubrik Cluster and optionally configure the required Cloud On options.
```py
def add_archive_azure(container, azure_access_key, storage_account_name, rsa_key, application_id=None, application_key=None, tenant_id=None, region=None, virtual_network_id=None, subnet_name=None, security_group_id=None, name='default', instance_type='default')
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| container  | str  | The name of the Azure storage container you wish to use as an archive. |         |
| azure_access_key  | str  | The access key for the storage account. |         |
| storage_account_name  | str  | The name of the Storage Account that the `container` belongs to. |         |
| rsa_key  | str  | The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| name  | str  | The name of the archive location used in the Rubrik GUI. If set to default the following naming convention will be used: Azure:`container` (default: {'default'}) (default: {'default'}) |         |    'default'     |
| instance_type  | str  | The Cloud Platform type of the archival location. (default: {'default'}) (choices: {'default', 'china', 'germany', 'government'}) |    'default', 'china', 'germany', 'government'     |    'default' (choices: {'default', 'china', 'germany', 'government'     |
| application_id  | str  | The Id of the application registered in Azure Active Directory. Only required when configuring Cloud On. (default: {None}) |         |    None     |
| application_key  | str  | The key of the application registered in Azure Active Directory. Only required when configuring Cloud On. (default: {None}) |         |    None     |
| tenant_id  | str  | The tenant Id, also known as the directory Id found under the Azure Active Directory properties. Only required when configuring Cloud On. (default: {None}) |         |    None     |
| region  | str  | The name of the Azure region where the `container` is located. Only required when configuring Cloud On. (default: {None}) (choices: {"westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"}) |    "westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"     |    None (choices: {"westus", "westus2", "centralus", "eastus", "eastus2", "northcentralus", "southcentralus", "westcentralus", "canadacentral", "canadaeast", "brazilsouth", "northeurope", "westeurope", "uksouth", "ukwest", "eastasia", "southeastasia", "japaneast", "japanwest", "australiaeast", "australiasoutheast", "centralindia", "southindia", "westindia", "koreacentral", "koreasouth"     |
| virtual_network_id  | str  | The virtual network Id used for Cloud On. (default: {None}) |         |    None     |
| subnet_name  | str  | The subnet name used for Cloud On. (default: {None}) |         |    None     |
| security_group_id  | str  | The security group Id used for Cloud On. (default: {None}) |         |    None     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`name`' archival location is already configured on the Rubrik Cluster." |
| dict  | The full API response for `POST /internal/archive/object_store'. |
