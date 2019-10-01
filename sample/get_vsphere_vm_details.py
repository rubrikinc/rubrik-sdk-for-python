import rubrik_cdm

id = 'VirtualMachine:::ID'

rubrik = rubrik_cdm.Connect()

get_vm_details = rubrik.get_vsphere_vm_details(id=id)
