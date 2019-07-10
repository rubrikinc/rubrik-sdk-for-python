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

# Volume Group


rubrik = rubrik_cdm.Connect()

# Note: To escape the "\" character, you need to use an extra "\". In
# other words, the "C:\" volume is shown as "C:\\" in the Python code.
object_name = ["C:\\", "D:\\"]
windows_host = "windows2016.rubrik.com"
sla_name = "Gold"

assign_sla = rubrik.assign_sla(object_name, sla_name, "volume_group", windows_host=windows_host)
