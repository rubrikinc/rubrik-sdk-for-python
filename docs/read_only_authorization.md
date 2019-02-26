# read_only_authorization

Grant read-only access to a specific user.
```py
def read_only_authorization(username, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username  | str  | The username you wish to grant read-only access to. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The user '`username`' already has read-only permissions. |
| dict  | The full API response from `POST /internal/authorization/role/read_only_admin`. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "python-sdk-read-only"

read_only_permission = rubrik.read_only_authorization(username)
```