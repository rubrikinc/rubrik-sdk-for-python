# azure_cloudout

Add a new Azure archival location to the Rubrik cluster.
```py
def azure_cloudout(container, azure_access_key, storage_account_name, rsa_key, archive_name='default', instance_type='default', timeout=180)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| container  | str  | The name of the Azure storage container you wish to use as an archive. The container name will automatically be lowercased and can not contain any of the following characters: `_\/*?%.:\|<>`. |         |
| azure_access_key  | str  | The access key for the Azure storage account. |         |
| storage_account_name  | str  | The name of the Storage Account that the `container` belongs to. |         |
| rsa_key  | str  | The RSA key that will be used to encrypt the archive data. A key can be generated through `openssl genrsa -out rubrik_encryption_key.pem 2048`. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| archive_name  | str  | The name of the archive location used in the Rubrik GUI. If set to `default`, the following naming convention will be used: "Azure:`container`"  |         |    default     |
| instance_type  | str  | The Cloud Platform type of the archival location.  |    default, china, germany, government     |    default      |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    180     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The '`name`' archival location is already configured on the Rubrik cluster. |
| dict  | The full API response for `POST /internal/archive/object_store`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

with open("/home/python-sdk-demo/rubrik_encryption_key.pem") as rsa_pem:
    rsa_key = rsa_pem.read()

storage_account_name = "pythonsdkdemo"
container = "pythonsdkdemocontainer"
azure_access_key = "ze=AIHW/Y2a7bee1MXXJelpN2clVa8E=YEw/IsCQE/LAecnyeeUMF6I/9mIi27oRBjyuiespqUHT928jW+TiWYA=="

cloudout = rubrik.azure_cloudout(container, azure_access_key, storage_account_name, rsa_key)
```