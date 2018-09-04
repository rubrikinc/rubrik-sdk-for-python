import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

snapshot = rubrik.on_demand_snapshot(vm_name, object_type)
