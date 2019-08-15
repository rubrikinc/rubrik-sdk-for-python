import rubrik_cdm

vm_name = "python-sdk-demo"

rubrik = rubrik_cdm.Connect()

live_mount = rubrik.get_vsphere_live_mount(vm_name)