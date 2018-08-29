# create_physical_fileset

Create a Fileset for a Linux or Windows machine.
```py
def create_physical_fileset(name, operating_system, include, exclude, exclude_exception, follow_network_shares=False, backup_hidden_folders=False, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str  | The name of the Fileset you wish to create. |         |
| operating_system  | str  | The Operating system type of Fileset you are created. (choices: {Linux, Windows.}) |    Linux, Windows.     |
| include  | list  | The full paths or wildcards that define the objects to include in the Fileset backup. Example: ['/usr/local', '*.pdf'] |         |
| exclude  | [type]  | The full paths or wildcards that define the objects to exclude from the Fileset backup. Example: ['/user/local/temp', '*.mov', '*.mp3'] |         |
| exclude_exception  | list  | The full paths or wildcards that define the objects that are exempt from the `excludes` variables.  Example: ['/company/*.mp4'] |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| follow_network_shares  | bool  | Include or exclude locally-mounted remote file systems from backups. (default: {False}) |         |    False     |
| backup_hidden_folders  | bool  | Include or exclude hidden folders inside locally-mounted remote file systems from backups. (default: {False}) |         |    False     |
| timeout  | int  | The timeout value for the API call that creates the Fileset. (default: {15}) |         |    15     |

## Returns
| Type | Description                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | If the Fileset is already present on the Rubrik Cluster the following is returned: The Rubrik Cluster already has a {`operating_system`} Fileset named '{`name`}' configured with the provided variables. |
| dict  | The full response for the `/internal/fileset_template/bulk` API endpoint. |
