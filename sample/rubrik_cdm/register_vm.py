import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "Python SDK"
register_vbs_on_bm = rubrik.register_vm(vm_name)