import rubrik_cdm

rubrik = rubrik_cdm.Connect()

mounted_vm_name = "python-sdk-demo"

live_unmount = rubrik.vsphere_live_unmount(mounted_vm_name)
