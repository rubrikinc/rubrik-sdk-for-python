import rubrik_cdm

vm_name = "python-sdk-demo"

rubrik = rubrik_cdm.Connect()

get_vm_snapshot = rubrik.get_vsphere_vm_snapshot(vm_name)
