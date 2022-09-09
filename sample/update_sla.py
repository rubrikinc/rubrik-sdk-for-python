import rubrik_cdm

rubrik = rubrik_cdm.Connect()

sla_name = "PythonSDK"
should_apply_to_existing_snapshots = True
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
replication_target = "REPLCLUSTER"
replication_retention_in_days = 30

update_sla = rubrik.update_sla(
    sla_name,
    should_apply_to_existing_snapshots,
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
    duration_hours,
    replication_target,
    replication_retention_in_days
)

print(update_sla)
