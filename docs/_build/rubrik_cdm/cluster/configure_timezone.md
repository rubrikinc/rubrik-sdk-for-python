# configure\_timezone

Configure the Rubrik cluster timezone.

```python
def configure_timezone(self, timezone, timeout=15):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| timezone | str | The timezone you wish the Rubrik cluster to use. | America/Anchorage, America/Araguaina, America/Barbados, America/Chicago, America/Denver, America/Los\_Angeles, America/Mexico\_City, America/New\_York, America/Noronha, America/Phoenix, America/Toronto, America/Vancouver, Asia/Bangkok, Asia/Dhaka, Asia/Dubai, Asia/Hong\_Kong, Asia/Karachi, Asia/Kathmandu, Asia/Kolkata, Asia/Magadan, Asia/Singapore, Asia/Tokyo, Atlantic/Cape\_Verde, Australia/Perth, Australia/Sydney, Europe/Amsterdam, Europe/Athens, Europe/London, Europe/Moscow, Pacific/Auckland, Pacific/Honolulu, Pacific/Midway, UTC |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |

## Returns

| Type | Return Value |
| :--- | :--- |
| str | No change required. The Rubrik cluster is already configured with '`timezone`' as it's timezone. |
| dict | The full API response for `PATCH /v1//cluster/me'` |

## Example

```python
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

timezone = "America/Chicago"

configure_timezone = rubrik.configure_timezone(timezone)
```

