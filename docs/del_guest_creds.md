# del_guest_creds

Deletes the guest credentials that are passed in if they exist.
```py
def del_guest_creds(username, domain=None, timeout=15)
```
## Arguments

| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| username | str  | Required - Username for guest credentials. |         |       |


## Keyword Arguments

| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| timeout | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 15      |
| domain | str  | The active directory domain if one is needed. |         | None      |

## Returns

| Type | Return Value                                                             |
|------|--------------------------------------------------------------------------|
| dict | The full API response from `POST /internal/vmware/guest_credential/{id}`.|
| str  | No change required. User not found.                                 |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

del_guest = rubrik.del_guest_creds("admin6","dantest4")

#print(del_guest)
```

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

#del_guest = rubrik.del_guest_creds("admin5")

#print(del_guest)
```