import rubrik_cdm

rubrik = rubrik_cdm.Connect()

# VMware Snapshot
vsphere_vm_name = "python-sdk-demo"
object_type = "vmware"
snapshot = rubrik.on_demand_snapshot(vsphere_vm_name, object_type)

# AHV Snapshot
ahv_vm_name = "python-sdk-demo"
object_type = "ahv"
snapshot = rubrik.on_demand_snapshot(ahv_vm_name, object_type)

# Physical Host Snapst
physical_host_name = "python-sdk-physical-demo"
object_type = "physical_host"
sla = "Gold"
fileset = "/etc"
host_os = "Linux"
snapshot = rubrik.on_demand_snapshot(physical_host_name, object_type, sla, fileset, host_os)

# Share
object_name = "python-sdk-share-demo"
object_type = "share"
sla = "Gold"
fileset = "/etc"
hostname = "python-sdk-demo"
share_type = "NFS"
snapshot = rubrik.on_demand_snapshot(object_name, object_type, sla, fileset, hostname=hostname, share_type=share_type)
