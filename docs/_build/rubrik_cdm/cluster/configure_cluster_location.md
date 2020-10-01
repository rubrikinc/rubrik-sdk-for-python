# configure\_cluster\_location

Configure cluster geolocation. Overwrites previously set value if different.

```python
def configure_cluster_location(self, location, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| location | str | Geolocation of the cluster. |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | If already configured with the same, the location is returned |
| dict | The full API response from `PATCH /cluster/me`. |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

rubrik.configure_cluster_location("St. Louis, Missouri")
```

