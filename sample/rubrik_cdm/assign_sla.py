# VMware

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
sla_name = "Gold"
object_type = "vmware"

assign_sla = rubrik.assign_sla(vm_name, sla_name, object_type)

# MSSQL


rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk.demo.com'
object_type = 'mssql_host'

sla_name = 'Gold'
log_backup_frequency_in_seconds = 600
log_retention_hours = 12
copy_only = False

assignsla = rubrik.assign_sla(
    object_name,
    sla_name,
    object_type,
    logBackupFrequencyInSeconds,
    logRetentionHours,
    copyOnly)

# Oracle Database


import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'HRDB50'
object_type = 'oracle_db'
hostname = 'python-sdk.demo.com'

sla_name = 'Gold'
log_backup_frequency_in_minutes = 30
log_retention_hours = 720
num_channels = 4

assignsla = rubrik.assign_sla(
    object_name,
    sla_name,
    object_type,
    log_backup_frequency_in_minutes=log_backup_frequency_in_minutes,
    log_retention_hours=log_retention_hours,
    num_channels=num_channels,
    hostname=hostname)

# Oracle Host


import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk.demo.com'
object_type = 'oracle_host'

sla_name = 'Gold'
log_backup_frequency_in_minutes = 30
log_retention_hours = 720
num_channels = 4

assignsla = rubrik.assign_sla(
    object_name,
    sla_name,
    object_type,
    log_backup_frequency_in_minutes=log_backup_frequency_in_minutes,
    log_retention_hours=log_retention_hours,
    num_channels=num_channels)

# Volume Group


rubrik = rubrik_cdm.Connect()

# Note: To escape the "\" character, you need to use an extra "\". In
# other words, the "C:\" volume is shown as "C:\\" in the Python code.
object_name = ["C:\\", "D:\\"]
windows_host = "windows2016.rubrik.com"
sla_name = "Gold"

assign_sla = rubrik.assign_sla(object_name, sla_name, "volume_group", windows_host=windows_host)

# Fileset


rubrik = rubrik_cdm.Connect()

object_name = 'nas_fileset'
object_type = 'fileset'

sla_name = 'Gold'
nas_host = 'nas-server.rubrik.com'
share = '/nas_share'

assign_sla = rubrik.assign_sla(object_name, sla_name, object_type, nas_host=nas_host, share=share)
