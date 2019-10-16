import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"

rubrik.vcenter_refresh_vm(vm_name)