# create_sla

Create a new SLA Domain.

```py
def create_sla(self, name, hourly_frequency=None, hourly_retention=None, daily_frequency=None, daily_retention=None, monthly_frequency=None, monthly_retention=None, yearly_frequency=None, yearly_retention=None, archive_name=None, retention_on_brik_in_days=None, instant_archive=False, starttime_hour=None, starttime_min=None, duration_hours=None, timeout=15):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| name  | str | The name of the new SLA Domain. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| hourly_frequency  | int | Hourly frequency to take backups.  |  | None |
| hourly_retention  | int | Number of hours to retain the hourly backups.  |  | None |
| daily_frequency  | int | Daily frequency to take backups.  |  | None |
| daily_retention  | int | Number of hours to retain the daily backups.  |  | None |
| monthly_frequency  | int | Monthly frequency to take backups.  |  | None |
| monthly_retention  | int | Number of hours to retain the monthly backups.  |  | None |
| yearly_frequency  | int | Yearly frequency to take backups.  |  | None |
| yearly_retention  | int | Number of hours to retain the yearly backups.  |  | None |
| archive_name  | str | The optional archive location you wish to configure on the SLA Domain. When populated, you must also provide a `retention_on_brik_in_days`.  |  | None |
| retention_on_brik_in_days  | int | The number of days you wish to keep the backups on the Rubrik cluster. When populated, you must also provide a `archive_name`.  |  | None |
| instant_archive=  | bool | Flag that determines whether or not to enable instant archive. Set to true to enable.  |  | False |
| starttime_hour  | int | (CDM 5.0+) Starting hour of allowed backup window.  |  | None |
| starttime_min  | int | (CDM 5.0+) Starting minute of allowed backup window. When populated, you must also provide a `starttime_min`.  |  | None |
| duration_hours  | int | (CDM 5.0+) Length of allowed backup window. When populated, you must also provide both `startime_min` and `starttime_hour`.  |  | None |
| timeout  | str | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 15 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The 'name' SLA Domain is already configured with the provided configuration. |
| dict | The full API response for `POST /v1/sla_domain`. |
| dict | The full API response for `POST /v2/sla_domain`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

sla_name = "PythonSDK"
hourly_frequency = 1
hourly_retention = 24
daily_frequency = 1
daily_retention = 30
monthly_frequency = 1
monthly_retention = 12
yearly_frequency = 1
yearly_retention = 5
archive_name = "AWS-S3-Bucket"
retention_on_brik_in_days = 15
instant_archive = True
starttime_hour = 0
starttime_min = 19
duration_hours = 12

create_sla = rubrik.create_sla(
    sla_name,
    hourly_frequency,
    hourly_retention,
    daily_frequency,
    daily_retention,
    monthly_frequency,
    monthly_retention,
    yearly_frequency,
    yearly_retention,
    archive_name,
    retention_on_brik_in_days,
    instant_archive,
    starttime_hour,
    starttime_min,
    duration_hours
)

print(create_sla)

```
