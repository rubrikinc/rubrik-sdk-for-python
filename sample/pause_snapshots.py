import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

pause_snapshot = rubrik.pause_snapshots(vm_name, object_type)
