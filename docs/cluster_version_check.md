# cluster_version_check

Determine if the Rubrik cluster is using running an earlier release than the provided CDM `minimum_cluster_version`. If the CDM version is an earlier release than the "clusterVersion", the following message error message is thrown: Error: The Rubrik cluster must be running CDM version {`minimum_cluster_version`} or later.

```py
def cluster_version_check(minimum_cluster_version, timeout=15)
```

## Arguments

| Name                    | Type  | Description                                                            | Choices |
|-------------------------|-------|------------------------------------------------------------------------|---------|
| minimum_cluster_version | float | The minimum required version of Rubrik CDM you wish ensure is running. |         |

## Keyword Arguments

| Name    | Type | Description                                                                                                  | Choices | Default |
|---------|------|--------------------------------------------------------------------------------------------------------------|---------|---------|
| timeout | int  | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |         | 15      |

## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

minimum_cluster_version = 5.0

node_names = rubrik.cluster_version_check(minimum_cluster_version)
```