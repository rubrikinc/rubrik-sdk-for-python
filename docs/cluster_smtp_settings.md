# cluster_smtp_settings

The Rubrik cluster uses email to send all notifications to local Rubrik cluster user accounts that have the Admin role. To do this the Rubrik cluster transfers the email messages to an SMTP server for delivery. This function will configure the Rubrik cluster with account information for the SMTP server to permit the Rubrik cluster to use the SMTP server for sending outgoing email.
```py
def cluster_smtp_settings(hostname, port, from_email, smtp_username, smtp_password, encryption="NONE", timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str  | Hostname of the SMTP server. |         |
| port  | int  | Incoming port on the SMTP server. Normally port 25, port 465, or port 587, depending upon the type of encryption used. |         |
| from_email  | str  |  The email address assigned to the account on the SMTP server |         |
| smtp_username  | str  | The username assigned to the account on the SMTP server |         |
| smtp_password  | str  | The password associated with the username |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| encryption  | str  |  The encryption protocol that the SMTP server requires for incoming SMTP connections  |    NONE, SSL, STARTTLS     |    NONE      |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster is already configured with the provided SMTP settings. |
| dict  | The full API response for `POST /internal/smtp_instance'` |
| dict  | The full API response for `PATCH /internal/smtp_instance/{id}'` |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

smtp_hostname = "smtp1"
port = 25
from_email = "python@sdk.com"
smtp_username = "pythonuser"
smtp_password = "pythonpass"

smtp_settings = rubrik.cluster_smtp_settings(smtp_hostname, port, from_email, smtp_username, smtp_password)
```