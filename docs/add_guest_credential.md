# add_guest_credential

Add a new guest credential to the Rubrik cluster.
```py
def add_guest_credential(username, password, domain=None, timeout=15):
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username | str  | The proxy username used for authentication.          |         |         |
| password | str  | The proxy password used for authentication.          |         |         |

## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| domain  | int  | The domain name of the account to be deleted. |         |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The account 'username' has already been added to the Rubrik cluster. |
| str  | No change required. The account 'username@domain' has already been added to the Rubrik cluster. |
| dict  | The full API response for `/vmware/guest_credential`. |

## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "pythonuser"
password = "python123!"

update_proxy = rubrik.add_guest_credential(username, password):
```
