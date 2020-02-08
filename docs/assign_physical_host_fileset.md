# assign_physical_host_fileset

Assign a Fileset to a Linux, Unix or Windows machine. If you have multiple Filesets with identical names, you will need to populate the Filesets properties (i.e this functions keyword arguments) to find a specific match. Filesets with identical names and properties are not supported.
```py
def assign_physical_host_fileset(hostname, fileset_name, operating_system, sla_name, include=None, exclude=None, exclude_exception=None, follow_network_shares=False, backup_hidden_folders=False, timeout=30)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| hostname  | str  | The hostname or IP Address of the physical host you wish to associate to the Fileset. |         |
| fileset_name  | str  | The name of the Fileset you wish to assign to the Linux, Unix or Windows host. |         |
| operating_system  | str  | The operating system of the physical host you are assigning a Fileset to.  |    Linux, Windows,UnixLike     |
| sla_name  | str  | The name of the SLA Domain to associate with the Fileset. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| include  | list  | The full paths or wildcards that define the objects to include in the Fileset backup (ex: ['/usr/local', '*.pdf']).  |         |    None     |
| exclude  | list  | The full paths or wildcards that define the objects to exclude from the Fileset backup (ex: ['/user/local/temp', '*.mov', '*.mp3']).  |         |    None     |
| exclude_exception  | list  | The full paths or wildcards that define the objects that are exempt from the `excludes` variables. (ex: ['/company/*.mp4']).  |         |    None     |
| follow_network_shares  | bool  | Include or exclude locally-mounted remote file systems from backups.  |         |    False     |
| backup_hidden_folders  | bool  | Include or exclude hidden folders inside locally-mounted remote file systems from backups.  |         |    False     |
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    30     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | No change required. The `operating_system` Fileset '`fileset_name`' is already assigned to the SLA Domain '`sla_name`' on the physical host '`hostname`'. |
| tuple  | When a new Fileset is created the following tuple will be returned: (Full API response from `POST /v1/fileset`, Full API response from `POST /v1/fileset/{id}`) |
| dict  | When the Fileset already exsits but is assigned to the wrong the SLA the Full API response from `POST `v1/fileset/{id}` is returned. |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"
fileset_name = "Python SDK"
operating_system = 'Linux'
sla = 'Gold'

assign_fileset = rubrik.assign_physical_host_fileset(hostname, fileset_name, operating_system, sla)
```
