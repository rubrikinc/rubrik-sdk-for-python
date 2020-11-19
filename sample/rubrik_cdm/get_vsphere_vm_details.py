import rubrik_cdm

vm_name = "python-sdk-demo"

rubrik = rubrik_cdm.Connect()

get_vm_details = rubrik.get_vsphere_vm_details(vm_name)
