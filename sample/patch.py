import rubrik

rubrik = rubrik.Connect()

vm_id = "VirtualMachine:::5008_f7c393f3-383-4b44-920-8cde7a9ae2bd:::0"

config = {}
config['configuredSlaDomainId'] = "0589c4e5-eeec-4ece-9922-2c9ceef7bec8"

change_vm_sla = rubrik.patch('v1', '/vmware/vm/{}'.format(vm_id), config)
