import rubrik

rubrik = rubrik.Connect()

vm_name = "python-sdk-demo"
date = "08-26-2018"
time = "12:11 AM"

instant_recovery = rubrik.vsphere_instant_recovery(vm_name, date, time)
