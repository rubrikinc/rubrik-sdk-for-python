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
    instant_archive
)

print(create_sla)
