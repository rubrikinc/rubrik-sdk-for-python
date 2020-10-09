import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"
fileset_name = "Python SDK"
operating_system = 'Linux'
sla = 'Gold'

assign_fileset = rubrik.assign_physical_host_fileset(hostname, fileset_name, operating_system, sla)
