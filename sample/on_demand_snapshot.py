import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

snapshot = rubrik.on_demand_snapshot(vm_name, object_type)
