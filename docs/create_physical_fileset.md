# create_physical_fileset

Create a Fileset for a Linux or Windows machine.
```py
def create_physical_fileset(name, operating_system, include, exclude, exclude_exception, follow_network_shares=False, backup_hidden_folders=False, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str  | The name of the Fileset you wish to create. |         |
| operating_system  | str  | The operating system type of the Fileset you are creating.  |    Linux, Windows.     |
| include  | list  | The full paths or wildcards that define the objects to include in the Fileset backup (ex: ['/usr/local', '*.pdf']). |         |
| exclude  | list  | The full paths or wildcards that define the objects to exclude from the Fileset backup (ex: ['/user/local/temp', '*.mov', '*.mp3']). |         |
| exclude_exception  | list  | The full paths or wildcards that define the objects that are exempt from the `excludes` variables. (ex. ['/company/*.mp4'). |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| follow_network_shares  | bool  | Include or exclude locally-mounted remote file systems from backups.  |         |    False     |
| backup_hidden_folders  | bool  | Include or exclude hidden folders inside locally-mounted remote file systems from backups.  |         |    False     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The Rubrik cluster already has a `operating_system` Fileset named '`name`' configured with the provided variables. |
| dict  | The full response for the `POST /internal/fileset_template/bulk` API endpoint. |
