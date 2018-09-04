import rubrik_cdm

rubrik = rubrik_cdm.Connect()

hostname = "python-sdk-demo"

add_host = rubrik.add_physical_host(hostname)
