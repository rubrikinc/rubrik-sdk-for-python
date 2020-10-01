# add\_guest\_credential

Add a new guest credential to the Rubrik cluster.

```python
def add_guest_credential(self, username, password, domain=None, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| username | str | The account username used for authentication. |  |
| password | str | The account password used for authentication. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| domain | int | The domain name of account password used for authentication. |  | None |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The account 'username' has already been added to the Rubrik cluster. |
| str | No change required. The account 'username@domain' has already been added to the Rubrik cluster. |
| dict | The full API response for `POST /v1/vmware/guest_credential`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

username = "pythonuser"
password = "python123!"

add_guest_credential = rubrik.add_guest_credential(username, password)
```

