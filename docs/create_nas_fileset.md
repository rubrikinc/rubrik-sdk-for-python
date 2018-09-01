# create_nas_fileset

Create a NAS Fileset.
```py
def create_nas_fileset(name, share_type, include, exclude, exclude_exception, follow_network_shares=False, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str  | The name of the Fileset you wish to create. |         |
| share_type  | str  | The type of NAS Share you wish to backup.  |    NFS, SMB     |
| include  | list  | The full paths or wildcards that define the objects to include in the Fileset backup. |         |
| exclude  | [type]  | The full paths or wildcards that define the objects to exclude from the Fileset backup. |         |
| exclude_exception  | [type]  | The full paths or wildcards that define the objects that are exempt from the `excludes` variables. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| follow_network_shares  | bool  | Include or exclude locally-mounted remote file systems from backups.  |         |    False     |
| timeout  | int  | The timeout value for the API call that creates the Fileset.  |         |    15     |

## Returns
| Type | Return Value                                                                                   |
|------|-----------------------------------------------------------------------------------------------|
| str  | If the Fileset is already present on the Rubrik Cluster the following is returned: The Rubrik Cluster already has a NAS Fileset named '{`name`}' configured with the provided variables. |
| dict  | The full response for the `/internal/fileset_template/bulk` API endpoint. |
