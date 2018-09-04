import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

vmware_id = rubrik.object_id(vm_name, object_type)
