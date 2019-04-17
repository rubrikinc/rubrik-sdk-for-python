# minimum_installed_cdm_version

Determine if the Rubrik cluster is running the provided CDM `cluster_version` or later. If the cluster is running an earlier release of CDM, `False` is returned. If the cluster is running the provided `cluster_version`, or a later release, `True` is returned.
```py
def minimum_installed_cdm_version(cluster_version, timeout=15)
```

## Arguments
| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| cluster_version  | float  | The minimum required version of Rubrik CDM you wish ensure is running. |         |
## Keyword Arguments
| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| timeout  | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |         |    15     |
## Example
```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

cluster_version = 5.0

node_names = rubrik.minimum_installed_cdm_version(cluster_version)
```