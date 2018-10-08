import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

#VMware Snapshot
snapshot = rubrik.on_demand_snapshot(vm_name, object_type)

# Physical Host Snapst
physical_host_name = "python-sdk-physical-demo"
object_type = "physical_host"
sla = "Gold"
fileset = "/etc"
host_os = "Linux"

snapshot = rubrik.on_demand_snapshot(physical_host_name, object_type, sla, fileset, host_os)
