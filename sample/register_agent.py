import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = 'python-sdk-demo'

result = rubrik.register_agent(vm_name)
