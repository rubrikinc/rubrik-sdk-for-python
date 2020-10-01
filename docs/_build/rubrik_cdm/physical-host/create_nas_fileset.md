# create\_nas\_fileset

Create a NAS Fileset.

```python
def create_nas_fileset(self, name, share_type, include, exclude, exclude_exception, follow_network_shares=False, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| name | str | The name of the Fileset you wish to create. |  |
| share\_type | str | The type of NAS Share you wish to backup. | NFS, SMB |
| include | list | The full paths or wildcards that define the objects to include in the Fileset backup. |  |
| exclude | list | The full paths or wildcards that define the objects to exclude from the Fileset backup. |  |
| exclude\_exception | list | The full paths or wildcards that define the objects that are exempt from the `excludes` variables. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| follow\_network\_shares | bool | Include or exclude locally-mounted remote file systems from backups. |  | False |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The Rubrik cluster already has a NAS Fileset named '`name`' configured with the provided variables. |
| dict | The full response for the `POST /internal/fileset_template/bulk` API endpoint. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

name = "Python SDK"
share_type = 'NFS'
include = ['/usr/local', '*.pdf']
exclude = ['/user/local/temp', '*.mov', '*.mp3', '*.mp4']
exclude_exception = ['/company/*.mp4']

new_fileset = rubrik.create_nas_fileset(name, share_type, include, exclude, exclude_exception)
```

