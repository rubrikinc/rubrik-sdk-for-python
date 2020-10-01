# create\_user

Create a new user on the Rubrik cluster

```python
def create_user(self, username, password, first_name=None, last_name=None, email_address=None, contact_number=None, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| username | str | The username for the user you wish to create. |  |
| password | str | The password for the user you wish to create. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| first\_name | str | The first name of the user you wish to create. |  | None |
| last\_name | str | The last name of the user you wish to create. |  | None |
| email\_address | str | The email address of the user you wish to create. |  | None |
| contact\_number | str | The contact number of the user you wish to create. |  | None |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The user '`username`' already exists on the Rubrik cluster |
| dict | The full API response from `POST /internal/user`. |

## Example

```python
import rubrik_cdm
rubrik = rubrik_cdm.Connect()

username = "python-sdk-user"
password = "RubrikPythonSDK"

create_user = rubrik.create_user(username, password)
```

