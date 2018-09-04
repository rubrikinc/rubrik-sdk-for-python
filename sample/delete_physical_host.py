import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"

delete_host = rubrik.delete_physical_host(hostname)
