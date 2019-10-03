import rubrik_cdm

vm_name = "python-sdk-demo"
path = '/etc/hosts'

rubrik = rubrik_cdm.Connect()

get_vm_file = rubrik.get_vsphere_vm_file(vm_name, path=path)
