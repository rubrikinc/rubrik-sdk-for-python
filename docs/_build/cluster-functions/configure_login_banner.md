# configure\_login\_banner

Configure the Login Banner Text on the Rubrik cluster.

```python
def configure_login_banner(self, banner, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| banner | str | The Login Banner Text you wish to see when the Rubrik cluster login page loads. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The Rubrik cluster is already configured with the login banner text '`banner`'. |
| dict | The full API response for `PUT /internal/cluster/me/login_banner'` |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

bannerText = "Welcome To Rubrik"
configure_banner = rubrik.configure_login_banner(bannerText)
```

