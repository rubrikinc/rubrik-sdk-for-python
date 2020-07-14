# VMware

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

vmware_id = rubrik.object_id(vm_name, object_type)

# Oracle Database

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk-demo'
object_type = 'oracle_db'
hostname = 'python-sdk.demo.com'

oracle_id = rubrik.object_id(object_name, object_type, hostname=hostname)

# Organization

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization'

organization_id = rubrik.object_id(object_name, object_type)

# Organization Role ID

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization_role_id'

organization_role_id = rubrik.object_id(object_name, object_type)

# Organization Admin Role

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'PythonSDKOrganization'
object_type = 'organization_admin_role'

organization_admin_role = rubrik.object_id(object_name, object_type)

# SLA

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

sla_name = "Gold"
sla_id = rubrik.object_id(sla_name, "sla")

# VMware Host

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vmware_host = "demo-esx01.rubrikdemo.com"
vmware_host_id = rubrik.object_id(vmware_host, "vmware_host")

# Physical Host

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

linux_physical_host = "linux-demo"
linux_physical_host_id = rubrik.object_id(linux_physical_host, "physical_host")

# Fileset Template

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

template_name = "Linux - All Files"
host_os = "Linux"

template_id = rubrik.object_id(template_name, "fileset_template", host_os=host_os)

# Managed Volume

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

managed_volume_name = "demo-managed-volume"
managed_volume_id = rubrik.object_id(managed_volume_name, "managed_volume")

# MSSQL DB

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

db_name = "DemoData"
host = "sql-demo-host"
instance = "sql-demo-instance"

db_id = rubrik.object_id(db_name, "mssql_db", mssql_instance=host, mssql_host=instance)

# MSSQL Instance

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

host = "sql-demo-host"
instance = "sql-demo-instance"

instance_id = rubrik.object_id(instance, "mssql_instance", mssql_host=host)

# MSSQL Availability Group

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ag_name = "demo-msql-ag"
host = "sql-demo-host"

ag_id = rubrik.object_id(ag_name, "mssql_availability_group", mssql_host=host)

# vCenter

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vcenter_name = "amer2-vcsa.rubrikdemo.com"

vcenter_id = rubrik.object_id(vcenter_name, "vcenter")

# AWS Native

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

aws_cloud_source_name = "AWS - amer2"

aws_cloud_source_name_id = rubrik.object_id(aws_cloud_source, "aws_native")

# Oracle Host

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

oracle_host_name = "demo-oracle-l2"

oracle_host_id = rubrik.object_id(oracle_host_name, "oracle_host")

# Share

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

nas_share_name = "/ntap_nfs"
share_hostname = "amer2-ntap01.rubrikdemo.com"
share_type = "NFS"

share_id = rubrik.object_id(nas_share_name, "share", hostname=share_hostname, share_type=share_type)

# Archival Location

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

archival_location_name = "Azure:demo-archive-container"

archival_location_id = rubrik.object_id(archival_location_name, "archival_location")

# AHV

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

ahv_vm_name = "ahv_demo-vm1"

ahv_vm_id = rubrik.object_id(ahv_vm_name, "ahv")

 
