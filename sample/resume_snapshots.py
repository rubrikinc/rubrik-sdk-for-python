import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
object_type = "vmware"

resume_snapshot = rubrik.resume_snapshots(vm_name, object_type)
