# delete_guest_credential

Delete a guest credential from the Rubrik cluster.

```py
def delete_guest_credential(self, username, domain=None, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username  | str | The account username to be deleted. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| domain  | int | The domain name of the account to be deleted.  |  | None |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The guest credential 'username' does not exist. |
| str | No change required. The guest credential 'username@domain' does not exist. |
| dict | The full API response for `POST /v1/vmware/guest_credential` |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "pythonuser"

delete_guest_credential = rubrik.delete_guest_credential(username)

```
