# add_guest_creds

Adds the guest credentials that are passed in if they don't already exist.
```py
def add_guest_creds(username, password, domain=None, timeout=15)
```
## Arguments

| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| username | str  | Required - Username for guest credentials. |         |       |
| password | str  | Required - Password for guest credentials. |         |       |

## Keyword Arguments

| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| timeout | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 15      |
| domain | str  | The active directory domain if one is needed. |         | None      |

## Returns

| Type | Return Value                                                             |
|------|--------------------------------------------------------------------------|
| dict | The full API response from `POST /internal/vmware/guest_credential/{id}`.|
| str  | No change required. User already exists.                                 |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

#guest = rubrik.add_guest_creds("admin6","password123","dantest6")

#print(guest)
```

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

#guest = rubrik.add_guest_creds("admin5","password123")

#print(guest)
```