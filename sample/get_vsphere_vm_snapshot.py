import rubrik_cdm

id = 'VirtualMachine:::ID'

rubrik = rubrik_cdm.Connect()

get_vm_snapshot = rubrik.get_vsphere_vm_snapshot(id=id)
