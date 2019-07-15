import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11 AM"

live_mount = rubrik.vsphere_live_mount(vm_name, date, time)