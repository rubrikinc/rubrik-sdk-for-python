# begin_managed_volume_snapshot

Open a managed volume for writes. All writes to the managed volume until the snapshot is ended will be part of its snapshot.

```py
def begin_managed_volume_snapshot(self, name, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str | The name of the Managed Volume to begin the snapshot on. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The Managed Volume '`name`' is already assigned in a writeable state. |
| dict | The full API response for `POST /managed_volume/{id}/begin_snapshot`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

managed_volume_name = 'MV1'

begin_snapshot = rubrik.begin_managed_volume_snapshot(managed_volume_name)

print(begin_snapshot)

```
