# configure_replication_private

Configure replication partner as specified by user using PRIVATE NETWORK (direct connection).

```py
def configure_replication_private(self, username, password, target_ip, ca_certificate=None, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| username  | str | Username for the TARGET cluster |  |
| password  | str | Password for the TARGET cluster |  |
| target_ip  | str | Address of one of the nodes of the TARGET cluster |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| ca_certificate  | str | CA certificiate used to perform TLS certificate validation  |  | None |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full API response from `POST /internal/replication/target`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

remote_cluster_user = "testuser"
remote_cluster_password = "testpassword"
remote_cluster_ip = "1.2.3.4"

new_replication = rubrik.configure_replication_private(remote_cluster_user, remote_cluster_password, remote_cluster_ip)

```
