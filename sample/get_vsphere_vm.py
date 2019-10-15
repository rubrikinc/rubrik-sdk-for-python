import rubrik_cdm

vm_name = 'python-sdk-demo'

rubrik = rubrik_cdm.Connect()

get_vsphere_vm = rubrik.get_vsphere_vm(name=vm_name)
